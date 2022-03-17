
"""
@author: TT
# Data Source link for email messages  
"""
import os
import math
#dir = '..............'  File Path
dic_legit = {} 
dic_spam = {} 
dic_all = {} 
dic_test = {}
count_legit = 0
count_spam = 0
count_all = 0
count_legit_word = 0
count_spam_word = 0
count_all_word = 0

#***Calculation of the probability of each coming word in being in legit messages
def prob_legit_word(word):
    alpha = 1
    #print("Number in legit_dic:",dic_legit["167"])
    #print(dic_legit[word])
    #print(count_legit)
    #print(count_legit_word)
    #print((k + dic_legit[word]) / ((2 * k) + count_legit))
    #print ((alpha + dic_legit[word]) / ((2 * alpha) + count_legit_word))
    return (alpha + dic_legit[word]) / ((2 * alpha) + count_legit_word)

#***Calculation of the probability of each coming word in being in spam messages
def prob_spam_word(word):
    alpha = 1
    #print("Number in spam_dic:",dic_spam["167"])
    #print(word)
    #print(dic_spam[word])
    #print(count_spam)
    
    return (alpha + dic_spam[word]) / ((2 * alpha) + count_spam_word)
   
#** Predict function *##
def predict(path_new):
    excluded_word = ["Subject:"]
    
    for root, dirs, files in os.walk(path_new):
        for name in files:
            #print(name)
            file_path = f"{root}\{name}"
            with open(file_path, 'r') as f:
                for line in f:
                        for word in line.split():
                            if word not in excluded_word:    
                                if word in dic_test:  
                                    dic_test[word] += 1 
                                    
                                else:
                                    dic_test[word] = 1
                                    
            log_p_spam = 0.0
            log_p_legit = 0.0

            for word in dic_all:  
                p_spam = prob_spam_word(word)
                p_legit = prob_legit_word(word)
                
                if word in dic_test: 
                    log_p_spam += math.log(p_spam)
                    log_p_legit += math.log(p_legit)       
                else:
                    log_p_spam += math.log(1 - p_spam)
                    log_p_legit += math.log(1 - p_legit)
                           
            p_if_spam = (math.exp(log_p_spam))
            p_if_legit = (math.exp(log_p_legit))
            return (p_if_spam / (p_if_spam + p_if_legit))

#****** Train Function ***####
def loopDir(path):
    
    count_all_word = 0
    excluded_word = ["Subject:"]
    
    global dic_all
    global dic_legit
    global dic_spam
    global count_legit
    global count_spam
    global count_legit_word
    global count_spam_word
    
    for root, dirs, files in os.walk(path):
        for name in files:

            if (name.__contains__("legit")):
                count_legit += 1  
                file_path = f"{root}\{name}"
                
                with open(file_path, 'r') as f:               
                    for line in f:
                        for word in line.split():
                            if word not in excluded_word:    
                                if word in dic_legit:  
                                    dic_legit[word] += 1 
                                    count_legit_word += 1
                                    count_all_word += 1
                                else:
                                    dic_legit[word] = 1
                                    count_legit_word += 1
                                    count_all_word += 1
                                if word in dic_all:
                                    dic_all[word] += 1
                                else:
                                    dic_all[word] = 1
            else:
                count_spam += 1
                file_path = f"{root}\{name}"
                
                with open(file_path, 'r') as f:  
                    for line in f:
                        for word in line.split():
                            if word not in excluded_word:    
                                if word in dic_spam:  
                                    dic_spam[word] += 1 
                                    count_spam_word += 1
                                    count_all_word += 1
                                else:
                                    dic_spam[word] = 1
                                    count_spam_word += 1
                                    count_all_word += 1
                                if word in dic_all:
                                    dic_all[word] += 1
                                else:
                                    dic_all[word] = 1
    for k in dic_legit:
        if k in dic_spam:
            continue
        else:
            dic_spam[k] = 1
            count_spam_word += 1
            count_all_word += 1
    
    for k in dic_spam:
        if k in dic_legit:
            continue
        else:
            dic_legit[k] = 1
            count_legit_word += 1
            count_all_word += 1
            
    
    print()
    #print("Cross Validation loop")
    #print("The number of legit messages is:",count_legit) 
    #print(dic_legit) 
    
    #print("................")
    #print("The number of spam messages is:",count_spam)
    #print(dic_spam)
    #print("The number of words in legit messages is:", count_legit_word)
    #print("The number of words in spam messages is:", count_spam_word)
    #print("The total number of words is:", count_all_word)
 
            
### *****  10-Fold Cross Validation ********** #### 

##********** Folder pu1 *********************# 

# dir = '.......................' # File Path for subfolder pu1
numbers = list(range(1, 11))  
      
for i in range(1,11):
    numbers.remove(i)
    
    test_number = i
    print("Cross Validation loop",i,"begins..")
    for j in range(9):
        
        path_new = dir + str(numbers[j])
        
        loopDir(path_new)
    path_test = dir + str(i)
    
    decision = predict(path_test)
    print("Precision for",i," fold is:",decision)
    print()
    numbers.append(i)

##********* Folder pu2 ****************#     
# dir = '.....................' # File Path for subfolder pu2
# numbers = list(range(1, 11))  
# print(numbers)       
# for i in range(1,11):
#     numbers.remove(i)
#     #print(numbers)
#     #print(len(numbers))
#     test_number = i
#     print("Cross Validation loop",i,"begins..")
#     for j in range(9):
#         
#         path_new = dir + str(numbers[j])
#         #print(path_new)
#         loopDir(path_new)
#     path_test = dir + str(i)
#     #print(path_test)
#     decision = predict(path_test)
#     print("Precision for",i," fold is:",decision)
#     print()
#     numbers.append(i)

##********* Folder pu3 ****************#     
# dir = '........................' #File Path for subfolder pu3
# numbers = list(range(1, 11))  
# print(numbers)       
# for i in range(1,11):
#     numbers.remove(i)
#     #print(numbers)
#     #print(len(numbers))
#     test_number = i
#     print("Cross Validation loop",i,"begins..")
#     for j in range(9):
#         #print(j)
#         path_new = dir + str(numbers[j])
#         #print(path_new)
#         loopDir(path_new)
#     path_test = dir + str(i)
#     #print(path_test)
#     decision = predict(path_test)
#     print("Precision for",i," fold is:",decision)
#     numbers.append(i)

##********* Folder pua ****************#     
# dir = '.........................' # #File Path for subfolder pua
# numbers = list(range(1, 11))  
# print(numbers)       
# for i in range(1,11):
#     numbers.remove(i)
#     #print(numbers)
#     #print(len(numbers))
#     test_number = i
#     print("Cross Validation loop",i,"begins..")
#     for j in range(9):
#         #print(j)
#         path_new = dir + str(numbers[j])
#         #print(path_new)
#         loopDir(path_new)
#     path_test = dir + str(i)
#     #print(path_test)
#     decision = predict(path_test)
#     print("Precision for",i," fold is:",decision)
#     print()
#     numbers.append(i)
            
