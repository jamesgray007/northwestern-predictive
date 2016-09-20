## Job to Binary
jad_to_binary = {'admin.': 1 ,'unknown': 0, 'unemployed': 0,
    'management':0 ,'housemaid': 0,'entrepreneur':0, 'student' : 0,
    'blue-collar':0 , 'self-employed' : 0, 'retired' :0 , 'technician':0 , 
    'services' : 0}

junkn_to_binary = {'admin.': 0 ,'unknown': 1, 'unemployed': 0,
    'management':0 ,'housemaid': 0,'entrepreneur':0, 'student' : 0,
    'blue-collar':0 , 'self-employed' : 0, 'retired' :0 , 'technician':0 , 
    'services' : 0}

junem_to_binary = {'admin.': 0 ,'unknown': 0, 'unemployed': 1,
    'management':0 ,'housemaid': 0,'entrepreneur':0, 'student' : 0,
    'blue-collar':0 , 'self-employed' : 0, 'retired' :0 , 'technician':0 , 
    'services' : 0}


jma_to_binary = {'admin.': 0 ,'unknown': 0, 'unemployed': 0,
    'management':1 ,'housemaid': 0,'entrepreneur':0, 'student' : 0,
    'blue-collar':0 , 'self-employed' : 0, 'retired' :0 , 'technician':0 , 
    'services' : 0}
    
    
jho_to_binary = {'admin.': 0 ,'unknown': 0, 'unemployed': 0,
    'management':0 ,'housemaid': 1,'entrepreneur':0, 'student' : 0,
    'blue-collar':0 , 'self-employed' : 0, 'retired' :0 , 'technician':0 , 
    'services' : 0}
    
    
jen_to_binary = {'admin.': 0 ,'unknown': 0, 'unemployed': 0,
    'management':0 ,'housemaid': 0,'entrepreneur':1, 'student' : 0,
    'blue-collar':0 , 'self-employed' : 0, 'retired' :0 , 'technician':0 , 
    'services' : 0}
    
    
jst_to_binary = {'admin.': 0 ,'unknown': 0, 'unemployed': 0,
    'management':0 ,'housemaid': 0,'entrepreneur':0, 'student' : 1,
    'blue-collar':0 , 'self-employed' : 0, 'retired' :0 , 'technician':0 , 
    'services' : 0}
    
jbl_to_binary = {'admin.': 0 ,'unknown': 0, 'unemployed': 0,
    'management':0 ,'housemaid': 0,'entrepreneur':0, 'student' : 0,
    'blue-collar':1 , 'self-employed' : 0, 'retired' :0 , 'technician':0 , 
    'services' : 0}
    
    
jse_to_binary = {'admin.': 0 ,'unknown': 0, 'unemployed': 0,
    'management':0 ,'housemaid': 0,'entrepreneur':0, 'student' : 0,
    'blue-collar':0 , 'self-employed' : 1, 'retired' :0 , 'technician':0 , 
    'services' : 0}

jre_to_binary = {'admin.': 0 ,'unknown': 0, 'unemployed': 0,
    'management':0 ,'housemaid': 0,'entrepreneur':0, 'student' : 0,
    'blue-collar':0 , 'self-employed' : 0, 'retired' : 1 , 'technician':0 , 
    'services' : 0}
       
jte_to_binary = {'admin.': 0 ,'unknown': 0, 'unemployed': 0,
    'management':0 ,'housemaid': 0,'entrepreneur':0, 'student' : 0,
    'blue-collar':0 , 'self-employed' : 0, 'retired' :0 , 'technician': 1 , 
    'services' : 0}
    
    
jser_to_binary = {'admin.': 0 ,'unknown': 0, 'unemployed': 0,
    'management':0 ,'housemaid': 0,'entrepreneur':0, 'student' : 0,
    'blue-collar':0 , 'self-employed' : 0, 'retired' :0 , 'technician':0 , 
    'services' : 1}
    
    
admin = bank['job'].map(jad_to_binary)
junknown = bank['job'].map(junkn_to_binary)
unemployed = bank['job'].map(junem_to_binary)
mana = bank['job'].map(jma_to_binary)
jhouse = bank['job'].map(jho_to_binary)
entre = bank['job'].map(jen_to_binary) 
student = bank['job'].map(jst_to_binary) 
blue = bank['job'].map(jbl_to_binary)
selfemp = bank['job'].map(jse_to_binary)
retired = bank['job'].map(jre_to_binary)
tech = bank['job'].map(jte_to_binary)
services = bank['job'].map(jser_to_binary) 
 
x = np.array(admin), np.array(junknown), np.array(unemployed), np.array(mana), 
    np.array(jhouse), np.array(entre), np.array(student), np.array(blue), 
    np.array(selfemp), np.array(retired), np.array(tech), np.array(services),
    ]).T
 