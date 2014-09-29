import csv
#Import Process
import re
#Deduplication
#Input is six csv files, each with their respective fax or email or wevbform stats
#output will be three lists of lists, of deduped and combined email, fax and webform stats

#convert the txt file into a list of lists
#This just shows the order of how stuff is stored in the superList
csvS = ['Email2.csv', 'Email3.csv', 'Fax2.csv', 'Fax3.csv', 'Web2.csv', 'Web3.csv']

def deduping(theList):
    listOLists = [theList[0],theList[3],theList[2],theList[5],theList[1],theList[4]]
    
    #Must convert strings to ints for columns 1,2,3 for Email and fax and 2,3,4 for Web
    for x in range(len(listOLists)):
        for y in range(len(listOLists[x])):
            if len(listOLists[x][y]) == 6:
                listOLists[x][y][1] = int(listOLists[x][y][1])
                listOLists[x][y][2] = int(listOLists[x][y][2])
                listOLists[x][y][3] = int(listOLists[x][y][3])
            else:
                listOLists[x][y][2] = int(listOLists[x][y][2])
                listOLists[x][y][3] = int(listOLists[x][y][3])
                listOLists[x][y][4] = int(listOLists[x][y][4])
                
    #now run a check
#    for x in range(len(listOLists)):
 #       for y in range(len(listOLists[x])):
  #          if len(listOLists[x][y]) == 6:
   #             if listOLists[x][y][1] + listOLists[x][y][2] != listOLists[x][y][3]:
    #                if x ==0:
     #                   print 'input ' + "email" + " Error!", listOLists[x][y]
      #              if x ==1:
       #                 print 'input ' + "email" + " Error!", listOLists[x][y]
        #            if x == 2:
         #               print 'input ' + "fax" + " Error!", listOLists[x][y]
          #          if x == 3:
           #             print 'input ' + "fax" + " Error!", listOLists[x][y]
            #else:
             #   if listOLists[x][y][2] + listOLists[x][y][3] != listOLists[x][y][4]:
              #      if x == 4:
               #         print 'input ' + "webform" + " Error!", listOLists[x][y]
                #    if x == 5 :
                 #       print 'input ' + "webform" + " Error!", listOLists[x][y]

    #now we will deduplicate and combine Email2 with Email3, Fax2 with Fax3, etc. 
    # This only deduplicates across the two clusters, not within them
    dedupedLists = list(listOLists)
    #run through the super list, checking the first two then the next two
    for x in range(0,len(listOLists),2):
        firstLength = range(len(listOLists[x]))
        secondLength = range(len(listOLists[x+1]))
        #check each term in the cluster3 liss
        for y in secondLength:
            #check against the terms in the cluster 2 lists
            for z in firstLength:
                #check the rep_id, the zeroeth term in each list
#                print y, listOLists[x+1][y][0], z, listOLists[x][z][0]#This is a check to measure efficiency, how often this got cycled
#                if len(listOLists[x][z][5]) == 'Mike Gatto':
 #                   print listOLists[x][z], listOLists[x+1][y] # This was to see what is compared to what. Not all terms are compared at this point, reason unknown
                if listOLists[x+1][y][0] == listOLists[x][z][0]:
                    #For email and fax
                    if len(listOLists[x][z]) == 6:
                        dedupedLists[x][z][1] += listOLists[x+1][y][1]
                        dedupedLists[x][z][2] += listOLists[x+1][y][2]
                        dedupedLists[x][z][3] += listOLists[x+1][y][3]
                        #succeeded so break
                        break
                    #For Webforms
                    else:
                        dedupedLists[x][z][2] += listOLists[x+1][y][2]
                        dedupedLists[x][z][3] += listOLists[x+1][y][3]
                        dedupedLists[x][z][4] += listOLists[x+1][y][4]
                        #succeeded so break
                        break
                #If there is no match I need to append to the list
                elif listOLists[x+1][y][0] < listOLists[x][z][0]:
                    dedupedLists[x] += [listOLists[x+1][y]]
                    break

    #truncate deduped lists to only have 0,2 and 4
    finalDeduped = []
    for x in range(len(dedupedLists)):
        if x % 2 == 0:
            finalDeduped += [dedupedLists[x]]
            
    #now we will do cleanup, remove consecutive duplicate rep_id's from within the clusters that have multiple Districts
    #search through all the lists
    
    for x in range(len(finalDeduped)):
        #The list of excess duplicate Rep_ID's
        stuffToBeDeleted = []
        #search through the length of the lst
        for y in range(len(finalDeduped[x])-1):
            #first check if it equals the previous term, if so continue the loop
            if y >= 1:
                if finalDeduped[x][y][0] == finalDeduped[x][y-1][0]:
                    continue
            #this while loop checks if two consecutive things have the same REP_ID
            n = 1
            #keeps checking until there are no more matches
            while finalDeduped[x][y][0] == finalDeduped[x][y+n][0]:
                #add to the list of deletions
#                print finalDeduped[x][y], finalDeduped[x][y+n] #check to see what is being compared
                stuffToBeDeleted += [finalDeduped[x][y+n]]
                #add one as long as y + n does not exceed the last index of the list
                if y + n < len(finalDeduped[x]) - 1:
                    n += 1
                else:
                    #end of data
                    break
        
        #Now delete for the individual list
        for z in range(len(stuffToBeDeleted)):
#            print x, stuffToBeDeleted, stuffToBeDeleted[z]
            finalDeduped[x].remove(stuffToBeDeleted[z])
    
    #now search through the whole list to combine non-consecutive REP_ID's that failed to combine in the first run through
    #Sort the list by REP_ID from smallest to greatest
    #the sorting algorithm, M is the datatable, p is the position we are checking
    def mergeSort(m,p):
        #Basecase
        if len(m) < 2:
            return m
        #set up the two halves
        mid = len(m)/2
        left = m[:mid]
        right = m[mid:]
        #Recursive call
        mergeSort(left,p)
        mergeSort(right,p)

        i = 0
        j = 0
        k = 0
        while i < len(left) and j < len(right):
            if left[i][p] > right[j][p]:
                m[k] = left[i]
                i += 1
            else:
                m[k] = right[j]
                j += 1
            k += 1
        
        while i < len(left):
            m[k] = left[i]
            i += 1
            k += 1
            
        while j < len(right):
            m[k] = right[j]
            j += 1
            k += 1 
        
    #Now we merge sort all three lists
    for x in range(len(finalDeduped)):
        mergeSort(finalDeduped[x],0)
            
    #now run through the whole list (Except the last term) and combine if they match
        #if match, add the numbers to the first term
        #remove the second term
    for x in range(len(finalDeduped)):
        toBeRemoved = []
        for y in range(len(finalDeduped[x])-1):
 #           print finalDeduped[x][y][0], finalDeduped[x][y+1][0]
            if finalDeduped[x][y][0] == finalDeduped[x][y+1][0]:
                #add second item to toBeRemoved
                toBeRemoved += [finalDeduped[x][y+1]]
                #For email and fax
                if len(finalDeduped[x][y]) == 6:
                    finalDeduped[x][y][1] += finalDeduped[x][y+1][1]
                    finalDeduped[x][y][2] += finalDeduped[x][y+1][2]
                    finalDeduped[x][y][3] += finalDeduped[x][y+1][3]
                #For Webforms
                else:
                    finalDeduped[x][y][2] += finalDeduped[x][y+1][2]
                    finalDeduped[x][y][3] += finalDeduped[x][y+1][3]
                    finalDeduped[x][y][4] += finalDeduped[x][y+1][4]
                    
        #remove items from toBeRemoved
        for z in range(len(toBeRemoved)):
            finalDeduped[x].remove(toBeRemoved[z])            
    
    #now remove rep_id from all and web_id from webforms #the first and first and second terms in the lists respectively
    for x in range(len(finalDeduped)):
        for y in range(len(finalDeduped[x])):
            #email and fax 
            if len(finalDeduped[x][y]) == 6:
                finalDeduped[x][y].remove(finalDeduped[x][y][0])
            #webforms
            else:
                finalDeduped[x][y].remove(finalDeduped[x][y][0])
                finalDeduped[x][y].remove(finalDeduped[x][y][0])
    
    #Now sort by bad from highest to lowest
    for x in range(len(finalDeduped)):
        mergeSort(finalDeduped[x],1)
        
    #Now trim the folloowing ':' of finalDeduped[x][y][4] if it has one
#    for x in range(len(finalDeduped)):
 #       for y in range(len(finalDeduped[x])):
  #          length = len(finalDeduped[x][y][4])
   #         if finalDeduped[x][y][4][length - 1] == ':':
    #            finalDeduped[x][y][4] = finalDeduped[x][y][4][:length - 1]
                
    #Now remove all  "Vacant" from email list. Vacant has 2 leading spaces
    toBeRemoved = []
    for y in range(len(finalDeduped[0])):
        if finalDeduped[0][y][3] == "  Vacant":
            toBeRemoved += [finalDeduped[0][y]]
            
    #remove items from toBeRemoved
    for z in range(len(toBeRemoved)):
        finalDeduped[0].remove(toBeRemoved[z])

    #now calculate the percentages of successes for each list
    for x in range(len(finalDeduped)):
        for y in range(len(finalDeduped[x])):
            z = float(finalDeduped[x][y][0])/finalDeduped[x][y][2]
#            z *= 100
            z = str(int(z * 100)) + '%'
            finalDeduped[x][y] += [z]
            
    #now reformat finalDeduped to have the final term% moved to position 3
    statHolder = []
    secondPart = []
    
    for x in range(len(finalDeduped)):
        for y in range(len(finalDeduped[x])):
            statHolder = finalDeduped[x][y][5]
            finalDeduped[x][y].remove(statHolder)
            secondPart = finalDeduped[x][y][3:]
            finalDeduped[x][y] = finalDeduped[x][y][0:3]
            finalDeduped[x][y] += [statHolder]
            finalDeduped[x][y] += secondPart
    
    #Now we will create a new table, and apend it to the database finalDeduped made up of the average percentages and totals
    #Order is Total, Email, Webform
    summary = []
    for x in [0,2,1]:
        tempList = []
        summationGood = 0
        summationBad = 0
        summationTotal = 0
        for y in range(len(finalDeduped[x])):
            summationGood += finalDeduped[x][y][0]
            summationBad += finalDeduped[x][y][1]
            summationTotal += finalDeduped[x][y][2]
        percentage = str(int(float(summationGood)/summationTotal * 100)) + '%'
        summary += [[summationGood, summationBad, summationTotal, percentage]]
    
    #Remove all those with 0 Bad
    toBeRemoved = []
    for x in range(len(finalDeduped)):
        for y in range(len(finalDeduped[x])):
            if finalDeduped[x][y][1] <= 0:
                toBeRemoved += [finalDeduped[x][y]]
        for z in range(len(toBeRemoved)):
            finalDeduped[x].remove(toBeRemoved[z])
        toBeRemoved = []
    
    #now create overall as its own list, then add summary to it
    summationGood = 0
    summationBad = 0
    summationTotal = 0
    for x in range(len(summary)):
        summationGood += summary[x][0]
        summationBad += summary[x][1]
        summationTotal += summary[x][2]
    percentage = str(int(float(summationGood)/summationTotal * 100)) + '%'
    overall = [summationGood, summationBad, summationTotal, percentage]
    sumFinal = [overall] + summary
    finalDeduped += [sumFinal]
    
    #Need to make each the same length, aka populate with blank lines of [[],[],[],[],[],[]] in the short two
    longest = 0
    for x in range(len(finalDeduped)):
        if len(finalDeduped[x]) > longest:
            longest = len(finalDeduped[x])
    for x in range(len(finalDeduped)):
        for y in range(longest):
            if longest > len(finalDeduped[x]):
                finalDeduped[x] += [['','','','','','']]
    
    #Now combine the three lists into one list of lists, where each list item in the superlist
    #is made of one item from each of the lists, #Order is changed to Email, Webform, Fax, Summary aka webform and fax are switched
    CSVReady = []
    for x in [0,2,1,3]:
        for y in range(len(finalDeduped[x])):
            if x == 0:
                CSVReady += [finalDeduped[x][y]]
            else:
                if len(CSVReady) > y:
                    CSVReady[y] += finalDeduped[x][y]
                else:
                    CSVReady += finalDeduped[x][y]
#    print CSVReady, len(CSVReady)#test
    
    #export all into CSV called rawDedupedData.csv
    with open('C:/Users/Joseph.White/Documents/1 Job/Advocacy/PythonScriptingFiles/rawDedupedData.csv', 'wb') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(CSVReady)
        
    #now run a check
#    for x in range(len(finalDeduped)):
 #       for y in range(len(finalDeduped[x])):
  #          if type(finalDeduped[x][y][0]) != int:
   #             continue
    #        if finalDeduped[x][y][0] + finalDeduped[x][y][1] != finalDeduped[x][y][2]:
     #           if x ==0:
      #              print "email" + " Error!", finalDeduped[x][y]
       #         if x == 2:
        #            print "webform" + " Error!", finalDeduped[x][y]
         #       if x == 1:
          #          print "fax" + " Error!", finalDeduped[x][y]
           #     if x == 3 :
            #        print "summary" + " Error!", finalDeduped[x][y]
    print 'rawDedupedData delivered!'
    return 'rawDedupedData delivered!'


#the goal is to pull data from the two text emails into a usable format the Autodedup can process
def dataPull():
    #Here we have two input files, both txt, originalCluster2.txt and originalCluster3.txt
    cluster2 = 'C:/Users/Joseph.White/Documents/1 Job/Advocacy/PythonScriptingFiles/originalCluster2.txt'
    cluster3 = 'C:/Users/Joseph.White/Documents/1 Job/Advocacy/PythonScriptingFiles/originalCluster3.txt'
    clusters = [cluster2, cluster3]

    #we need to turn these two text files into a list of strings, each string being its own line. 
    with open('C:/Users/Joseph.White/Documents/1 Job/Advocacy/PythonScriptingFiles/Daily Advocacy Data Summary Report - cluster2.txt', 'r') as myfile:
        lines = list(myfile)
        clusters[0] = lines
        
    with open('C:/Users/Joseph.White/Documents/1 Job/Advocacy/PythonScriptingFiles/Daily Advocacy Data Summary Report - cluster3.txt', 'r') as myfile:
        lines = list(myfile)
        clusters[1] = lines
    #the new list of six clusters
    listOLists = [[],[],[],[],[],[]]
    #find breakpoints in the list
    for x in range(len(clusters)):
        ind1 = clusters[x].index('Advocacy data E-MAIL statistics\n')
        ind2 = clusters[x].index('Advocacy data WEBFORM statistics\n')
        ind3 = clusters[x].index('Advocacy data FAX statistics\n')

        ind4 = len(clusters[x])
        
        #now assign values to list of lists correct for excess lines around the breakpoints
        if x == 0:
            listOLists[0] = clusters[x][(ind1 + 4):(ind2 - 5)]
            listOLists[1] = clusters[x][(ind2 + 4):(ind3 - 5)]
            listOLists[2] = clusters[x][(ind3 + 4):(ind4 - 8)]
        if x == 1:
            listOLists[3] = clusters[x][(ind1 + 4):(ind2 - 5)]
            listOLists[4] = clusters[x][(ind2 + 4):(ind3 - 5)]
            listOLists[5] = clusters[x][(ind3 + 4):(ind4 - 8)]
    #now chomp off the \n from the end of the lines
    for x in range(len(listOLists)):
        for y in range(len(listOLists[x])):
            listOLists[x][y] = listOLists[x][y][:-1]
            #Now we need to split along \t and : 
            listOLists[x][y] = re.split('\t\t|\t|:  |:\t',listOLists[x][y])    
    return listOLists
    
deduping(dataPull())