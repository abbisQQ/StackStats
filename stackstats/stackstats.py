import datetime
import time
import requests
import json
import argparse
import operator



def main():
    #Using argparse for the arguments

    parser = argparse.ArgumentParser(description="This is a python app that can calculate statistics using the stack exchange api's data")
    parser.add_argument("--since", type=str, required=True, help="Starting date and time to search")
    parser.add_argument("--until", type=str, required=True, help="Ending date and time to search")
    parser.add_argument("--output-format", type=str, required=True, help="Which format the results will come in.",default='json')
    args= parser.parse_args()


    #variables 
    count = 0
    score = 0
    accepted_answers=0
    unique_questions_ids=[]
    id_and_score={}
    ids_for_url_usage=""
    comments = []


    #convert to datetime
    from_time = datetime.datetime.strptime(args.since, '%Y-%m-%d %H:%M:%S')
    to_time = datetime.datetime.strptime(args.until, '%Y-%m-%d %H:%M:%S')


    #This is the final dayTime as we need to convert to Unix epoch thats the time passed since is the number of seconds that have elapsed since January 1, 1970

    from_time  = int(time.mktime(from_time.timetuple()))
    to_time = int(time.mktime(to_time.timetuple()))


    # Making a call to stack exchange api and getting back the json data which in python come in a dictionary
    url = 'https://api.stackexchange.com/2.2/answers?fromdate='+str(from_time)+'&todate='+str(to_time)+'&order=asc&sort=activity&site=stackoverflow'
    data = requests.get(url)
    data = data.json()


    for item in data['items']:    
        count+=1
        if item["is_accepted"]==True:
            questionID=item['question_id']
            score+= item["score"]
            accepted_answers +=1
            #A dictionary that will containg the answer id and it's score     
            id_and_score[item['answer_id']] = item['score']        
            #the json data contains duplicates, to get rid of them we apply the next 2 lines of code
            if not questionID in unique_questions_ids:
                unique_questions_ids.append(questionID)

    #sorting the dictionary by value if we need to sort by key we could use itemgetter(0) in our case we also need reverse so we start from the biggest number
    sorted_id_and_score = sorted(id_and_score.items(), key=operator.itemgetter(1), reverse=True)
    sorted_id_and_score = sorted_id_and_score[:10] # gets the 10 elements if they are more than 10 in that dictionary


    sorted_id_and_scoreDic =  dict(sorted_id_and_score)
    average_score = float("%.1f" %(score/float(accepted_answers)))
    answers_per_questions =   float("%.1f" %(accepted_answers/float(len(unique_questions_ids))))


    for item in sorted_id_and_scoreDic:
        ids_for_url_usage += str(item)+";"
    #ids must be seperated by ; but the last id dosen't need one 
    ids_for_url_usage =  ids_for_url_usage[:-1]


    #We are getting the comments
    comments_url = 'https://api.stackexchange.com/2.2/answers/'+ids_for_url_usage+'/comments?order=desc&sort=creation&site=stackoverflow'
    comments_data = requests.get(comments_url)
    comments_data = comments_data.json()



    for item in comments_data['items']:
        comments.append(item['post_id'])


    if len(sorted_id_and_score) < 10: # if we have less than 10 answers, take all the answer_ids
        top_ten_answers = [int(i[0]) for i in sorted_id_and_score] # gets the [0] thats the key or in our case the id for each item in sorted_id_and_score
    else: # if we have >= 10 answers, get the first 10 answer_ids (highest scores)
        top_ten_answers = []
        flag = 0
        for i in sorted_id_and_score:
            if x < 9:
                top_ten_answers.append(i[0])
                print i[0]
                x +=1


    commentCount = {} # dictionary that contains first 10 answers with their comment count
    for answer in top_ten_answers:
        #for  each answer 'post_id' get the comments count
        count = comments.count(answer) 
        commentCount[answer] = count

    if args.output_format=="json":
        #Finally we present the results to our users in JSON format
        results={"total_accepted_answers":accepted_answers,"accepted_answers_average_score":average_score,"average_answers_per_question":answers_per_questions,"top_ten_answers_comment_count":commentCount}
        print json.dumps(results, indent=2)
    elif args.output_format=="tabular":
        print "| total_accepted_answers | accepted_answers_average_score | average_answers_per_question | top_ten_answers_comment_count |"
        print "| "+str(accepted_answers) +(" "*(23-len(str(accepted_answers)))) +"| " + str(average_score) +(" "*(31-len(str(average_score)))) +"| "+ str(answers_per_questions) +(" "*(29-len(str(answers_per_questions))))+"| " +"answer_id: comment_count      |" 
        for key, value in commentCount.iteritems():
            print "| " +(" "*23)+"| "+(" "*31)+"| "+(" "*29)+"| "+ str(key) +": "+str(value) +(" "*(30-len(str(key) +": "+str(value))))+"|"
            


if __name__=="__main__":
    try:
        main()
    except:
        print "Oups something went wrong check your input, internet connection and the StackExchange API"

