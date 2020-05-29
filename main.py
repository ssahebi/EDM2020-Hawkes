import warnings; warnings.simplefilter('ignore')
import pandas as pd
import os
import sys
module_path = os.path.abspath(os.path.join('..'))
if module_path not in sys.path:
    sys.path.append(module_path)
from Hawkes.utils import *
from modeling import *

assignment_fact,assignment_dim,sub_a,sub_a_dim,discussion,conversation,wiki\
,discussion_topic,discussion_dim,conversation_dim,discussion_topic_dim,\
sub_comment_dim,sub_comment,enrollment,enrollment_dim = importdata()

course_id = 770000832960058
sub_quiz_time = create_quiz_sub_time(course_id, sub_q, sub_q_dim, quiz_fact, quiz_dim)
sub_assignment_time = create_assignment_sub_time(course_id, sub_a, sub_a_dim, assignment_fact, assignment_dim)
dis = create_discussion_time(course_id = 770000832960058,discussion=discussion,discussion_dim = discussion_dim)
dis_topic = create_discussion_topic_time(course_id,discussion_topic,discussion_topic_dim)
conv = create_conversation_time(course_id,conversation,conversation_dim)
comm = create_comment_time(course_id,sub_comment,sub_comment_dim)
a = create_assignment_sub_time(course_id, sub_a, sub_a_dim, assignment_fact, assignment_dim)
q = create_quiz_sub_time(course_id, sub_q, sub_q_dim, quiz_fact, quiz_dim)

R_q, R_a, R_dis, R_wiki, R_conv = create_requests_time(course_id, enrollment,enrollment_dim)
Dis = create_discussion_time(course_id, discussion, discussion_dim)
Dis_topic = create_discussion_topic_time(course_id, discussion_topic, discussion_topic_dim)
Conv = create_conversation_time(course_id, conversation, conversation_dim)
Comment = create_comment_time(course_id, sub_comment, sub_comment_dim)

A_list = ['assignment_r',
                  'assignment_due_at',
                  'assignmentsub_created_at','quiz_r']
# Q_list = ['quiz_r',
#           'quiz_due_at',
#           'quizsub_created_at']

C_list = ['created_at_dis',
          'created_at_topic',
          'dis_r',
          'created_at_comment',
          'created_at_msg',
          'conv_r']
W_list = ['wiki_r']
D_list_a = ['assignment_due_at']
# D_list_q = ['quiz_due_at']

Dimensions_3= dict(zip(['Deadline','Submissions','Activities'],[D_list_a, A_list, C_list+W_list]))
# agg = agg_time(R_a, a, R_q, q, Dis, Dis_topic, R_dis, Comment, Conv, R_conv, R_wiki, Dimensions=None)
# subD
agg_lists = [D_list_a, A_list, C_list, W_list]
column_names = ['Deadline_agg', 'Assignment_agg', 'Communication_agg',
                'Wiki_agg']
Dimensions_6 = dict(zip(column_names, agg_lists))


# for Dimensions in [Dimensions_3,Dimensions_6][:1]:
#     if Dimensions==Dimensions_3:
#         ddl = ['Deadline_timestamp']
#     else:
#         ddl = ['Deadline_agg_a_timestamp', 'Deadline_agg_q_timestamp']
#
#     agg = agg_time(R_a, a, R_q, q, Dis, Dis_topic, R_dis, Comment, Conv, R_conv, R_wiki, Dimensions=Dimensions)
#
#     df = time2timestamp(agg, course_id, enrollment,enrollment_dim)
#     # print(df)
#     for f in ['all_ddls','sub_ddls','other'][1:2]:
#
#         df = pre_hawkess(df=df, course_id=course_id, flavor=f, assignment_dim=assignment_dim, quiz_dim=quiz_dim, quiz_fact=quiz_fact,deadlines_name=ddl)
#         for learnertype in ['HawkesADM4','HawkesExpKern'][0:1]:
#
#             print('processing model: ' + f + ' with dimensions ' + str(len(Dimensions.keys())) + ' using ' + learnertype)
#             # print(df)
#
#             model_hawkes(df=df, learnertype=learnertype, decay=[1,6,24], Dimensions=Dimensions,flavor = f,def_low = 0.25,def_high = 0.75)
# #
