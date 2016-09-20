/*
Function library for all message detail page javascript operations
includes AJAX loads for thread div and message div
includes all UI switches and js functions in links
on the page, and includes settings for stickiness of UI switches.
*/

var gCurPos = "bottom";
var gCurTreeSize = "100";
var gCurTop = "0";

// retrieve the persisted current position of the message div
function getCurrPos()
{
  return gCurPos;
}

// get a handle to the div where the message is currently displaying
function getMessageDiv()
{
    var myBottom = document.getElementById('message');
    var myTop = document.getElementById('message_upper');
    if (getCurrPos() == "bottom")
    {
        return myBottom;
    }
    return myTop;
}

// GLOBAL variables
var treeDiv = document.getElementById('tree');
var messageDiv = getMessageDiv();
var currentDiv = messageDiv;
var curtop; // set in jsp to determine where to scroll to

var isInitialLoad = true;

var Message = {};

// get a handle to the div where the message is currently NOT displaying
function getOtherMessageDiv()
{
    var myBottom = document.getElementById('message');
    var myTop = document.getElementById('message_upper');
    if (getCurrPos() == "top")
    {
        return myBottom;
    }
    return myTop;
}


//log any problems with the AJAX request
function logError (message)
{
 document.getElementById('message').innerHTML = message;
}

//encapsulate and return a generic function that handles waiting and issues with the AJAX request
function getReadyStateHandler(req, responseHandler)

{
    return function ()
    {
        if (req.readyState == 4)
        {
            if (req.status == 200)
            {
                // all good, pass the response text on
                responseHandler( req.responseText);
            }
            else
            {
                logError("Error processing request: " + req.status);
            }
        }
    };
}


//retrieve the persistent tree size, or the default 100px
function getTreeSize()
{
  return gCurTreeSize;
}

//persist the tree size
function setTreeSize( cValue )
{
  MessageManagementService.setDetailPageSetting( "msg_detail_treesize", cValue );
  gCurTreeSize = cValue;
}

//hide the whole tree div
function minimizeThreads()
{
    var treediv   = document.getElementById("tree");
    var selectDiv = document.getElementById("selectBox");
    var linkDiv   = document.getElementById("hideImg");

    var topListActionBar     = document.getElementById("top_list_action_bar");
    var bottomListActionBar  = document.getElementById("bottom_list_action_bar");

    treediv.style.display="none";
    if (selectDiv)
    {
      selectDiv.style.display="none";
    }
    if (topListActionBar)
    {
      topListActionBar.style.display="none";
    }
    if (bottomListActionBar)
    {
      bottomListActionBar.style.display="none";
    }
    window.currHide="none";
    linkDiv.src="/images/ci/misc/collapse_db.gif";
    document.getElementById("minmaxImg").src="/images/ci/misc/expand_db.gif";
    linkDiv.alt= window.restoreLabel;
    linkDiv.parentNode.title= window.restoreLabel;
    setTreeSize(0);
}

//set to full height
function expandTreeSize ()
{
    var fixthreads = document.getElementById("tree");
    fixthreads.style.height = '';
    document.getElementById("minmaxImg").src="/images/ci/misc/collapse_db.gif";
    document.getElementById("minmaxImg").alt= window.restoreLabel;
    document.getElementById("minmaxImg").parentNode.title= window.collapseLabel;
    setTreeSize(-1);
}


//retrieve the persisted scroll position of the thread tree
function getCurrentOffset ()
{
  return parseInt( gCurTop, 10 );
}

//set to arbitrary pixel size
function collapseTreeSize ( pixels )
{
    var fixthreads = document.getElementById("tree");

    fixthreads.style.height   = pixels + "px";
    fixthreads.scrollTop = getCurrentOffset();
    document.getElementById("minmaxImg").src = "/images/ci/misc/expand_db.gif";
    document.getElementById("minmaxImg").alt = window.expandLabel;
    document.getElementById("minmaxImg").parentNode.title = window.expandLabel;
    setTreeSize(pixels);
}

//just change the arrow image based on string "up" or "down"
function fixSwapImg (direction)
{
    if (direction == "up")
    {
        document.getElementById("swapImg").src="/images/ci/misc/up_db.gif";
        document.getElementById("swapImg").alt= window.upLabel;
        document.getElementById("swapImg").parentNode.title= window.upLabel;
    }
    else
    {
        document.getElementById("swapImg").src="/images/ci/misc/down_db.gif";
        document.getElementById("swapImg").alt= window.downLabel;
        document.getElementById("swapImg").parentNode.title= window.downLabel;
    }
}

//retrieve the original sticky settings and apply them
function initTreeSize ()
{
    var originalSize = getTreeSize();
    if (originalSize === 0) { minimizeThreads(); }
    else if (originalSize < 0)  { expandTreeSize(); }
    else if (originalSize > 0)  { collapseTreeSize(100); }

    // if the message div is at the top, fix the margin and the arrow image
    if (getCurrPos() == "top")
    {
        fixSwapImg("up");
       // document.getElementById("message_upper").style.marginTop="10px";
    }
}

function resizeTreeAndEvalScripts( respText )
{
    // reset the tree size; display as expanded (w/o scrollbars) or collapsed
    initTreeSize();
    // NOTE: this was assuming that the script block that contains the message count
    // updating code is the last one in the HTML returned for the tree
    // BUT when the cloud is on (or at least the sample-social-learning fake-cloud)
    // then there are more script blocks making the one we want "not the last".
    // Instead, look for the specific block we care about and execute it.
    // TODO: I'm not sure what the cloud is expecting to have executed in this context
    // so the cloud team needs to test whatever they're adding to the discussion board
    // and maybe just have this block execute ALL script blocks instead of just the one we care about.
    var scripts = respText.extractScripts("script");
    for (var i=0;i<scripts.length;i++)
    {
      if (scripts[i].indexOf("updateMessageCounts") !== -1)
      {
        // update the total/unread counts. see message_tree
        eval( scripts[i] );
      }
    }
}

//actually put the retrieved HTML in the destination DIV
//called after marking msgs read/unread and flagging messages
function populateTreeDivWOMsg( respText )
{
var treeDiv = $('tree');
//do any preprocess parsing needed
treeDiv.innerHTML = respText;
resizeTreeAndEvalScripts.defer( respText );
}

/**
 * Function to update message counts when the tree is reloaded.
 * @param int totalCount the new total count
 * @param int unreadCount the new unread count (if > 0, collection link will be activated )
 */
function updateMessageCounts( totalCount, unreadCount )
{
  if ( totalCount )
  {
    var totalSpan = document.getElementById("totalPostsCount");
    totalSpan.innerHTML = totalCount;
  }

  if ( unreadCount !== undefined )
  {
    var unreadSpan = document.getElementById("unreadPostsCount");
    if ( unreadCount > 0 )
    {
      // collectUnreadUrl is defined in message_detail page
      unreadSpan.innerHTML = '<a href=\"' + window.collectUnreadUrl + "\">" + unreadCount + "</a>";
    }
    else
    {
      unreadSpan.innerHTML = unreadCount;
    }
  }
}

/**
 * Function to decrement the unread count after clicking on an unread message
 */
function decrementUnreadCount()
{
  var unreadSpan = document.getElementById("unreadPostsCount");

  var anchor = unreadSpan.getElementsByTagName("a");
  var currentUnreadCount;
  if ( anchor.length > 0 )
  {
    currentUnreadCount = parseInt( anchor[0].innerHTML, 10 );
  }
  else
  {
    currentUnreadCount = parseInt( unreadSpan.innerHTML, 10 );
  }

  if ( currentUnreadCount > 0 )
  {
    updateMessageCounts( null, currentUnreadCount - 1);
  }
}

//wrapper for loadDiv for the message. Also makes sure the other div stays empty
function loadMessage()
{
    var messageDiv = getMessageDiv();
    window.loadDiv ( window.messageUrl, messageDiv, false);
    getOtherMessageDiv().innerHTML = "";
}

//actually put the retrieved HTML in the destination DIV
//called by first loads of message detail page or for refresh
function populateTreeDiv( respText )
{
populateTreeDivWOMsg( respText );


// mark current message style as READ and update readUnread count on page
// this is done for display purposes, but is saved to the database when loadMessage() (called below)
// makes the round trip to the displayMessage() struts action
var currRowId = document.getElementById("treeForm").old_tr_id.value;
var currRow = document.getElementById(currRowId);
if ( currRow.style.fontWeight != "normal" )
{
 currRow.style.fontWeight="normal";
 decrementUnreadCount();
}

loadMessage();
}

//updates the page with previous and next post links
function updatePageWithPreviousNextPostLinks()
{

  var allAnchorTagsInThreadTree = document.getElementById("treeForm").getElementsByTagName("a");

  // array to hold all of the anchor tags that surround the subject of each post in the tree
  var targetATagElements = [];
  var index = 0;
  var currElement;

  // populate targetATagElements
  for(var i=0; i < allAnchorTagsInThreadTree.length; i++)
  {
    currElement = allAnchorTagsInThreadTree[i];
    var currElementId = currElement.id;
    if( currElementId.match("msg_link_area_") )
    {
      targetATagElements[index] = currElement;
      index++;
    }
  }

  // if there are more than one msg in the tree, proceed to calculate the previous
  // and next post links, otherwise, there isn't any previous and next posts so
  // do not bother calculating
  if( targetATagElements.length > 1 )
  {
    var previousPostId = "";
    var nextPostId = "";

    // determine previous and next message links
    for(var j=0; j < targetATagElements.length; j++)
    {
      currElement = targetATagElements[j];
      if( currElement.id == ("msg_link_area_" + window.currentMessageId))
      {
        if( j === 0 )
        {
          previousPostId = "";
        }
        else
        {
          previousPostId = targetATagElements[j-1].id;
        }

        if( j == ( targetATagElements.length - 1 ) )
        {
          nextPostId = "";
        }
        else
        {
          nextPostId = targetATagElements[j+1].id;
        }

        break;

      }
    }

    // create the previous post link and add it to the document
    var previousPostAnchorTagEleFromTree = document.getElementById( previousPostId );
    if(previousPostAnchorTagEleFromTree)
    {
      $( 'previousPostUrlArea' ).show();
      $( 'previousPostUrlArea_b' ).show();
      $( 'previousPostUrl' ).href = previousPostAnchorTagEleFromTree.href;
      $( 'previousPostUrl_b' ).href = previousPostAnchorTagEleFromTree.href;
    }
    else
    {
      $( 'previousPostUrlArea' ).hide();
      $( 'previousPostUrlArea_b' ).hide();
      $( 'previousPostUrl' ).href = '#';
      $( 'previousPostUrl_b' ).href = '#';
    }

    // create the next post link and add it to the document
    var nextPostAnchorTagEleFromTree = document.getElementById( nextPostId );
    if(nextPostAnchorTagEleFromTree)
    {
      $( 'nextPostUrlArea' ).show();
      $( 'nextPostUrlArea_b' ).show();
      $( 'nextPostUrl' ).href = nextPostAnchorTagEleFromTree.href;
      $( 'nextPostUrl_b' ).href = nextPostAnchorTagEleFromTree.href;
    }
    else
    {
      $( 'nextPostUrlArea' ).hide();
      $( 'nextPostUrlArea_b' ).hide();
      $( 'nextPostUrl' ).href = '#';
      $( 'nextPostUrl_b' ).href = '#';
    }
  }
}

//actually put the retrieved HTML in the destination DIV
function populateMessageDiv( respText )
{
 // do any preprocess parsing needed
 getMessageDiv().innerHTML = respText.stripScripts();
 // evauate any JavaScript in the response
 page.globalEvalScripts( respText, false );
 updatePageWithPreviousNextPostLinks();
 // wire any lightboxes in the message div
 new page.LightboxInitializer( 'lb', getMessageDiv() );
 //focus on the message
 if ( !isInitialLoad )
 {
   getMessageDiv().focus();
 }
 isInitialLoad = false;
}

//return the AJAX object used to retrieve the URL
function newXMLHttpRequest()
{
    var xmlreq = false;
    if (window.XMLHttpRequest)
    {
        xmlreq = new XMLHttpRequest();
    }
    else if (window.ActiveXObject)
    {
        try
        {
            xmlreq = new ActiveXObject("Msxml2.XMLHTTP");
        }
        catch (e1)
        {
            try
            {
                xmlreq = new ActiveXObject("Microsoft.XMLHTTP");
            }
            catch (e2)
            {
                // swallow
            }
        }
    }
    return xmlreq;
}

/*
 * load the contents of an href into the destination element
 * @param href URL to send through
 * @param destination tree DIV or message DIV
 * @param loadTreeWithoutMsg boolean determining which populate tree method to set as callback function;
 *                           if true, it calls the populateTreeDivWOMsg, else populateTreeDiv;
 *                           this value is only used if the destination is the tree DIV
 * @param isPost boolean specifying whether to use POST or GET.  Default is GET.
 */
function loadDiv( href , destination, loadTreeWithoutMsg, isPost )
{
    var usePostMethod = typeof isPost !== 'undefined' && isPost;
    var requestHref = href + "&req_timestamp=" + new Date().getTime() + '_' + Math.random();
    var req = newXMLHttpRequest();
    // the handler function takes the object, the function to handle the response, and the destination div
    var handlerFunction;
    if (destination.id == "tree")
    {
        if(loadTreeWithoutMsg)
        {
          handlerFunction = getReadyStateHandler( req, populateTreeDivWOMsg );
        }
        else
        {
          handlerFunction = getReadyStateHandler( req, populateTreeDiv );
        }
        currentDiv = treeDiv;
    }
    else
    {
        handlerFunction = getReadyStateHandler( req, populateMessageDiv );
    }
    req.onreadystatechange = handlerFunction;

    if (usePostMethod )
    {
      var sessionParamAndValue = "session=" + getCookie('JSESSIONID');
      var splitRequestHref = requestHref.split('?');
      var baseUrl = "";
      var queryString = "";
      if ( splitRequestHref && splitRequestHref.length == 2 )
      {
        baseUrl = splitRequestHref[0];
        queryString = splitRequestHref[1] + '&' + sessionParamAndValue;
      }
      else
      {
        baseUrl = requestHref;
        queryString = sessionParamAndValue;
      }
      // XSRF protection
      req.open( "POST", baseUrl, true );
      req.setRequestHeader( "Content-Type", "application/x-www-form-urlencoded");

      req.send(queryString);
    }
    else
    {
      req.open ("GET",requestHref,true);
      req.send("");
    }
}

// post the contents of a form to an href, load the results into the element with ID of destStr
function loadPostDiv ( href, myForm, destStr)
{
    var req = newXMLHttpRequest();
    var handlerFunction;
    if (destStr == "tree")
    {
        handlerFunction = getReadyStateHandler( req, populateTreeDivWOMsg );
    }
    else
    {
        handlerFunction = getReadyStateHandler( req, populateMessageDiv );
    }

    // XSRF protection
    href += '&session=' + getCookie( 'JSESSIONID' );

    req.onreadystatechange = handlerFunction;
    req.open( "POST", href, true );
    req.setRequestHeader( "Content-Type", "application/x-www-form-urlencoded");
    var params = "";
    for (var i = 0; i < myForm.elements.length; i++)
    {
        if ( myForm.elements[i].type != "checkbox" || ( myForm.elements[i].type == "checkbox" && myForm.elements[i].checked ) )
        {
            params += myForm.elements[i].name + "=" + escape(myForm.elements[i].value) +"&";
        }
    }
    req.send(params);
}


// called by "Show/Hide" original post link in message_frame.jsp and message_edit.jsp.
// make the selection sticky in session using ajax function
function changeLink(YN)
{
    if (YN == "Y")
    {
        document.getElementById("linkD").style.display = "none";
        document.getElementById("linkH").style.display = "block";
      MessageParentPostShowOptionService.setShowParentPost("true");
    } else
    {
        document.getElementById("linkD").style.display = "block";
        document.getElementById("linkH").style.display = "none";
      MessageParentPostShowOptionService.setShowParentPost("false");
    }
}

// wrapper for loadDiv for the thread tree
function loadTree()
{
    var treeDiv = document.getElementById('tree');
    loadDiv ( window.treeUrl,treeDiv, false);
}

//expand/collapse operations to a (potentially) arbitrary pixel size
function changeTreeSize ( pixels )
{
    var treediv    = document.getElementById("tree");
    var selectDiv  = document.getElementById("selectBox");
    var linkDiv    = document.getElementById("hideImg");

    var topListActionBar     = document.getElementById("top_list_action_bar");
    var bottomListActionBar  = document.getElementById("bottom_list_action_bar");


    treediv.style.display="block";
    if (selectDiv)
    {
      selectDiv.style.display="block";
    }
    if (topListActionBar)
    {
      topListActionBar.style.display="block";
    }
    if (bottomListActionBar)
    {
      bottomListActionBar.style.display="block";
    }
    linkDiv.src = "/images/ci/misc/hide_db.gif";
    linkDiv.alt = window.hideLabel;
    linkDiv.parentNode.title = window.hideLabel;

    // fixthreads.style.height=="100px"
    if( getTreeSize() > 0 )
    {
        expandTreeSize();
    }
    else
    {
        collapseTreeSize ( pixels );
    }

}

// catcher function for the expand/collapse button
function enbigulator()
{
    changeTreeSize(100);
}

//persist the current position of the message div
function setCurrPos(cValue)
{
  MessageManagementService.setDetailPageSetting("msg_detail_position", cValue );
  gCurPos = cValue;
}

// catcher function for the swap up/swap down button pair
function moveMessage()
{
    var divContent;
    if(getCurrPos()=="bottom")
    {
        divContent=document.getElementById("message").innerHTML;
        document.getElementById("message_upper").innerHTML=divContent;
        document.getElementById("message").innerHTML="";
        //document.getElementById("message_upper").style.marginTop="10px";
        fixSwapImg("up");
        setCurrPos("top");
    }
    else
    {
        divContent=document.getElementById("message_upper").innerHTML;
        document.getElementById("message").innerHTML=divContent;
      //  document.getElementById("message_upper").innerHTML="<img src='/images/ci/misc/shim.gif' width='1' height='1' alt=''>";
        document.getElementById("message_upper").innerHTML="";
    //document.getElementById("message_upper").style.marginTop="0";
        fixSwapImg("down");
        setCurrPos("bottom");
    }
}

//put the treeDiv back (TODO: setTreeSize might should be 100 in some cases)
function unMinimizeThreads()
{
    var treediv   = document.getElementById("tree");
    var selectDiv = document.getElementById("selectBox");
    var linkDiv   = document.getElementById("hideImg");
    var minmaxDiv = document.getElementById("minmaxLink");

    var topListActionBar     = document.getElementById("top_list_action_bar");
    var bottomListActionBar  = document.getElementById("bottom_list_action_bar");

    treediv.style.display="block";
    if (selectDiv)
    {
      selectDiv.style.display="block";
    }
    if (topListActionBar)
    {
      topListActionBar.style.display="block";
    }
    if (bottomListActionBar)
    {
      bottomListActionBar.style.display="block";
    }
    window.currHide = "block";
    linkDiv.alt= window.hideLabel;
    linkDiv.parentNode.title= window.hideLabel;
    linkDiv.src="/images/ci/misc/hide_db.gif";
    setTreeSize(-1);
}

// catcher function for the minimize/maximize button set
function hideMessage()
{
    var treediv = document.getElementById("tree");
    if(treediv.style.display=="block" ||
       treediv.style.display=="" ||
       treediv.style.display=="undefined")
    {
        minimizeThreads();
    }
    else
    {
        unMinimizeThreads();
    }
}

// persist the scroll position
function setCurrentOffset( val )
{
    var fixthreads = document.getElementById("tree");
    var curOff = document.getElementById(val).offsetTop;
    curOff = curOff + 2;

    MessageManagementService.setDetailPageSetting( "msg_detail_top", curOff );
    gCurTop = curOff;
}


// MESSAGE TREE FUNCTIONS


// turn on all the checkboxes
function selectAllCheckboxes(theForm)
{
    for(var i = 0; i < theForm.elements.length; i++)
    {
        if(theForm.elements[i].type == "checkbox")
        {
            theForm.elements[i].checked = true;
        }
    }
}


// turn off all the checkboxes
function selectNoneCheckboxes(theForm)
{
    for(var i = 0; i < theForm.elements.length; i++)
    {
        if(theForm.elements[i].type == "checkbox")
        {
            theForm.elements[i].checked = false;
        }
    }
}


// set all the checkboxes the opposite way
function selectInvertCheckboxes(theForm)
{
    for(var i = 0; i < theForm.elements.length; i++)
    {
        if(theForm.elements[i].type == "checkbox")
        {
            if (theForm.elements[i].checked)
            {
                theForm.elements[i].checked = false;
            }
            else
            {
                theForm.elements[i].checked = true;
            }
        }
    }
}


// collection of checkbox methods based on the element ID of the form and the picker
function updateCheckboxSelections(myForm, myPicker)
{
    var theForm = document.getElementById(myForm);
    var thePicker = document.getElementById(myPicker);
    if (thePicker.value ==  "selectall")
    {
        selectAllCheckboxes(theForm);
    }
    else if (thePicker.value ==  "selectnone")
    {
        selectNoneCheckboxes(theForm);
    }
    else if (thePicker.value ==  "invert")
    {
        selectInvertCheckboxes(theForm);
    }
    else
    {
        return;
    }
}


// validation function to make sure at least one checkbox is checked
// and submit the result to the collectUrl (defined in the jsp)
function validateCollect(theForm)
{
    var isValidate = false;
    for(var i = 0; i < theForm.elements.length; i++)
    {
        if(theForm.elements[i].type == "checkbox")
        {
            if (theForm.elements[i].checked)
            {
                isValidate = true;
                break;
            }
        }
    }
    if (isValidate)
    {
        // XSRF protection
        var url = window.collectUrl + '&session=' + getCookie( 'JSESSIONID' );

        theForm.action = url;
        theForm.submit();
    }
    else
    {
        alert( window.strSelect);
    }
}
// validation function to make sure at least one checkbox is checked
// and submit the result to the markReadUrl (defined in the jsp)
function validateMarkRead(theForm)
{
    var isValidate = false;
    for(var i = 0; i < theForm.elements.length; i++)
    {
        if(theForm.elements[i].type == "checkbox")
        {
            if (theForm.elements[i].checked)
            {
                isValidate = true;
            }
        }
    }

    if (isValidate)
    {
        loadPostDiv( window.markReadUrl, theForm, 'tree');
    }
    else
    {
        alert( window.strSelect);
    }
}
// validation function to make sure at least one checkbox is checked
// and submit the result to the markUnreadUrl (defined in the jsp)
function validateMarkUnread(theForm)
{
    var isValidate = false;
    for(var i = 0; i < theForm.elements.length; i++)
    {
        if(theForm.elements[i].type == "checkbox")
        {
            if (theForm.elements[i].checked)
            {
                isValidate = true;
            }
        }
    }

    if (isValidate)
    {
        loadPostDiv( window.markUnreadUrl, theForm, 'tree');
    }
    else
    {
        alert( window.strSelect);
    }
}

/**
 * Toggles the flag/clear flag state on the current message
 * @param {Object} msgId Id of the message to toggle the state for
 * @param {Object} doRequest whether to persist the change to the server (call with false if you only want to change the state of the button on the page )
 * @param {Object} forcedValue value to force the flag status to be ( true will cause the "clear flag" option to appear, false the "add flag" )
 */
function toggleFlag( msgId, doRequest, forcedValue )
{
  var link1 = document.getElementById('flagToggleLinkTop');
  var link2 = document.getElementById('flagToggleLinkBottom');

  var test;

  if ( forcedValue )
  {
    test = forcedValue;
  }
  else
  {
    test = ( link1.innerHTML.indexOf( window.flagOnLabel ) >= 0 );
  }

  var queryString = "&message_id="+msgId+"&formCBs=" + msgId;
  var usePostMethod = true;
  if ( test )
  {
    if ( doRequest )
    {
      loadDiv( window.addFlagUrl + queryString , document.getElementById('tree'), true, usePostMethod );
    }
    link1.innerHTML = window.flagOffLabel;
    link2.innerHTML = window.flagOffLabel;
  }
  else
  {
    if ( doRequest )
    {
      loadDiv( window.clearFlagUrl + queryString, document.getElementById('tree'), true, usePostMethod );
    }
    link1.innerHTML = window.flagOnLabel;
    link2.innerHTML = window.flagOnLabel;
  }

}

// validation function to make sure at least one checkbox is checked
// and submit the result to the addFlagUrl (defined in the jsp)
function validateAddFlag()
{
    var theForm = document.getElementById('treeForm');
    var isValidate = false;
    for(var i = 0; i < theForm.elements.length; i++)
    {
        if(theForm.elements[i].type == "checkbox")
        {
            if (theForm.elements[i].checked)
            {
                isValidate = true;
                if ( theForm.elements[i].value == window.currentMessageId )
                {
                    toggleFlag( window.currentMessageId, false, true );
                    break;
                }
            }
        }
    }

    if (isValidate)
    {
        loadPostDiv( window.addFlagUrl+ "&message_id=" + window.currentMessageId, theForm,'tree');
    }
    else
    {
        alert( window.strSelect);
    }
}


// validation function to make sure at least one checkbox is checked
// and submit the result to the clearFlagUrl (defined in the jsp)
function validateClearFlag()
{
    var theForm = document.getElementById('treeForm');
    var isValidate = false;
    for(var i = 0; i < theForm.elements.length; i++)
    {
        if(theForm.elements[i].type == "checkbox")
        {
            if (theForm.elements[i].checked)
            {
                isValidate = true;
                if ( theForm.elements[i].value == window.currentMessageId )
                {
                    toggleFlag( window.currentMessageId, false, false );
                    break;
                }
            }
        }
    }

    if (isValidate)
    {
        loadPostDiv( window.clearFlagUrl + "&message_id=" + window.currentMessageId, theForm, 'tree');
    }
    else
    {
        alert( window.strSelect);
    }
}

// function for the reply button
function reply(msg_id)
{
    location.href=window.replyUrl+msg_id;
}

// function for the reply button
function replyWithQuote(msg_id)
{
    location.href=window.replyUrl+msg_id+"&quote=true";
}


// pass the search box form to the searchUrl (defined in the JSP)
function executeSearch()
{
    if (validateForm(document.dateAvailabilityForm) && calendar.DateTimePicker.validatePickers() )
    {
        document.dateAvailabilityForm.action = window.searchUrl;
        document.dateAvailabilityForm.submit();
    }
}


// synonym function for the refresh button
Message.refreshTree = function ()
{
    loadTree();
};


// catcher function for pressing return in the keyword search box
function checkSearch(evt)
{
    var name = navigator.appName;
    evt = evt ? evt : (window.event ? window.event : null);
    if (name == "Microsoft Internet Explorer")
    {
        if (evt.keyCode == 13)
        {
            evt.keyCode = 9;
            executeSearch();
        }
    }
    else
    {
        if (evt.which == 13)
        {
            executeSearch();
        }
    }
}

//highlight the selected message row, de-highlight the previous row
function changeBGColor(tr_id)
{
    var whichEl = document.getElementById(tr_id);
    whichEl.style.background="#E2EBF6";
    whichEl.style.fontWeight="normal";
    setCurrentOffset(tr_id);

    var oldVal = document.getElementById("treeForm").old_tr_id.value;
    var whichE2 = document.getElementById(oldVal);
    whichE2.style.background="#ffffff";
    document.getElementById("treeForm").old_tr_id.value = tr_id;
}

//expands tree, showing all msg rows if row passed in is hidden (display: none)
function expandTreeCheck(tr_id)
{
    // if current msg is hidden, expand the entire tree
    var currentMsgRowEle = document.getElementById(tr_id);
    //var currentMsgRowEle = currRow;
    if(currentMsgRowEle.style.display=="none")
    {
      //alert("current msg is hidden, proceed tdo expand all tree!");

      // get all message row elements, set them all to display
      var msgRowElements = document.getElementById("treeForm").getElementsByTagName("TR");
      for(var i = 0; i<msgRowElements.length; i++)
      {
        var currElement = msgRowElements[i];

        // if the current row is hidden, show it again
        if( currElement.style.display=="none")
        {
          currElement.style.display="block";
        }

        // get the toggle icon of the current row, if it's the collapsed icon, set it to the expanded icon
        var currElementToggleIcon = document.getElementById(currElement.id+'_img');
        if(currElementToggleIcon && (currElementToggleIcon.src).match("/images/ci/icons/treecontrol/rplus.gif") )
        {
          currElementToggleIcon.src="/images/ci/icons/treecontrol/rminus.gif";
          currElementToggleIcon.alt=window.collapseThreadLabel;
        }

      }
    }
}

// catcher function for clicking a new message in the thread tree (jump around)
function display(thread_id, msg_id,tr_id)
{
    var destination = getMessageDiv();
    window.currentMessageId = msg_id;
    var getUrl = window.displayUrl+"&message_id="+msg_id+"&thread_id="+thread_id;
    loadDiv(getUrl, destination, false);
    // decrement the unread count if the message was unread (i.e. bolded )
    if ( document.getElementById( tr_id ).style.fontWeight != "normal" )
    {
      decrementUnreadCount();
    }
    changeBGColor(tr_id);
    expandTreeCheck(tr_id);
}

//fix indentation in the thread tree
function changeSpan()
{
    var spanColl = $$( '#treeForm span.expandCollapse' )
    var whichEl1;
    for (var i = 0; i < spanColl.length; i++)
    {
        whichEl1 = spanColl[ i ];
        if (i + 1 < spanColl.length)
        {
            var whichEl2 = spanColl[ i + 1 ];
            if ( whichEl2.id.indexOf(whichEl1.id) < 0)
            {
                eval("document.getElementById('"+whichEl1.id+"').innerHTML=" + "\"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\";");
            }
        }
    }
    eval("document.getElementById('"+whichEl1.id+"').innerHTML="+"\"&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;\";");
}

// expand-collapse in the thread tree
function toggle(pID)
{
    var isOn = false;
    if(eval("document.getElementById('treeForm').Flag" + pID + ".value == \"0\""))
    {
      eval("document.getElementById('treeForm').Flag" + pID + ".value = \"1\"");
      eval("document.getElementById('sp"+pID+"').innerHTML="+"\"<a href=javascript:toggle('" + pID + "')><img id='"+pID+"_img' src='/images/ci/icons/treecontrol/rminus.gif' alt='"+window.collapseThreadLabel+"' border='0'></a>" + "\";");
      isOn = false;
    }
    else
    {
      eval("document.getElementById('treeForm').Flag" + pID + ".value = \"0\"");
      eval("document.getElementById('sp"+pID+"').innerHTML="+"\"<a href=javascript:toggle('" + pID + "')><img id='"+pID+"_img' src='/images/ci/icons/treecontrol/rplus.gif' alt='"+window.expandThreadLabel+"' border='0'></a>" + "\";");
      isOn = true;
    }

    // all message table rows in tree
    var trColl = document.getElementById("treeForm").getElementsByTagName("TR");

    for (var i=0; i<trColl.length; i++)
    {
        var whichEl = trColl.item(i);
        if ( pID == whichEl.id)
        {
          continue;
        }
        if (whichEl.id.indexOf(pID) === 0 )
        {
            if( isOn )
            {
                if (whichEl.id.split("_").length - 1 >= pID.split("_").length)
                {
                    whichEl.style.display = "none";
                    eval("document.getElementById('sp"+whichEl.id+"').innerHTML="+"\"<a href=javascript:toggle('" + whichEl.id + "')><img id='"+whichEl.id+"_img' src='/images/ci/icons/treecontrol/rplus.gif' alt='"+window.expandThreadLabel+"' border='0'></a>" + "\";");
                    eval("document.getElementById('treeForm').Flag" + whichEl.id + ".value = \"0\"");
                }
            }
            else
            {
                if (whichEl.id.split("_").length - 1 == pID.split("_").length)
                {
                    whichEl.style.display = "block";
                    eval("document.getElementById('treeForm').Flag" + whichEl.id + ".value = \"0\"");
                }
            }
        }
    }
    changeSpan();
}


// MESSAGE FRAME FUNCTIONS

// called by modify button, uses modifyUrl (set in JSP)
function modify(msg_id)
{
    document.location.href=window.modifyUrl+msg_id;
}


// called by remove button, uses removeUrl and confirm message (set in JSP)
function remove(msg_id)
{
    if (confirm(window.strConfirmRemove))
    {
      var messageFrameForm = $('messageFrameForm');
      messageFrameForm.action=window.removeUrl+msg_id;
      messageFrameForm.submit();
    }
}

function subUnSub()
{
   document.location = window.subscribeUrl;
}


// called by Rate button - load raeUrl (set on JSP), passing rate_post pulldown value in message Div
function rate(msg_id)
{
  loadDiv( window.rateUrl + $('messageFrameForm').rate_post.value + "&message_id=" + msg_id, getMessageDiv(), false );
}


function rateMessage(msg_id, rating)
{
  loadDiv(window.rateUrl + rating + "&message_id=" + msg_id, getMessageDiv(), false );

  var ratingList = $(msg_id + '.rating');
  ratingList.removeClassName('star0');
  ratingList.removeClassName('star1');
  ratingList.removeClassName('star2');
  ratingList.removeClassName('star3');
  ratingList.removeClassName('star4');
  ratingList.removeClassName('star5');
  ratingList.addClassName('star' + rating);
}

function toggleParentMessageDisplay()
{
  var e = $('parentMessage');
  var i = $('parentMessageDisplayImage');
  if (e && i)
  {
    if (e.visible())
    {
      MessageParentPostShowOptionService.setShowParentPost("false");
      e.hide();
      i.src = '/images/ci/ng/more_options_dark.gif';
      i.title = i.alt = '${bbFn:jsEncode(strSPP)}';
    }
    else
    {
      MessageParentPostShowOptionService.setShowParentPost("true");
      e.show();
      i.src = '/images/ci/ng/less_options_dark.gif';
      i.title = i.alt = '${bbFn:jsEncode(strHPP)}';
    }
  }
}

function cbSelectAll(selector)
{
  $A($$(selector)).each(function(item, index) {
     item.checked = true;
   });
}

function cbSelectNone(selector)
{
  $A($$(selector)).each(function(item, index) {
     item.checked = false;
   });
}

function cbSelectInverse(selector)
{
  $A($$(selector)).each(function(item, index) {
     item.checked = !item.checked;
   });
}
