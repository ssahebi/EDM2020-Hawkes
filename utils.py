import pandas as pd
import numpy as np
import datetime
from os import listdir
from os.path import isfile, join
import os

def importdata():
    # quiz_fact = pd.read_csv('../datasets/CANVAS/tables/quiz_fact.csv', sep=None)
    quiz_dim = pd.read_csv('../datasets/CANVAS/tables/sample_course/770000832960058/quiz_dim.csv', sep=None)
    # sub_q = pd.read_csv('../datasets/CANVAS/tables/quiz_submission_fact.csv', sep=None)
    # sub_q_dim = pd.read_csv('../datasets/CANVAS/tables/quiz_submission_dim.csv', sep=None)

    # print("quiz data imported")
    # import assignment data

    assignment_fact = pd.read_csv('../datasets/CANVAS/tables/sample_course/770000832960058/assignment_fact.csv',
                                  sep=None)
    assignment_dim = pd.read_csv('../datasets/CANVAS/tables/sample_course/770000832960058/assignment_dim.csv', sep=None)
    assignment_dim['assignment_id'] = assignment_dim['id'].tolist()
    sub_a = pd.read_csv('../datasets/CANVAS/tables/sample_course/770000832960058/submission_fact.csv', sep=None)
    sub_a_dim = pd.read_csv('../datasets/CANVAS/tables/sample_course/770000832960058//submission_dim.csv', sep=None)
    print("assignment data imported")

    # import activities
    discussion = pd.read_csv('../datasets/CANVAS/tables/sample_course/770000832960058/discussion_entry_fact.csv',
                             sep=None)
    conversation = pd.read_csv(
        '../datasets/CANVAS/tables/sample_course/770000832960058/conversation_message_participant_fact.csv',
        sep=None)
    wiki = pd.read_csv('../datasets/CANVAS/tables/wiki_page_fact.csv', sep=None)
    discussion_topic = pd.read_csv('../datasets/CANVAS/tables/sample_course/770000832960058/discussion_topic_fact.csv',
                                   sep=None)
    discussion_dim = pd.read_csv('../datasets/CANVAS/tables/sample_course/770000832960058/discussion_entry_dim.csv',
                                 sep=None)
    conversation_dim = pd.read_csv(
        '../datasets/CANVAS/tables/sample_course/770000832960058/conversation_message_dim.csv', sep=None)
    discussion_topic_dim = pd.read_csv(
        '../datasets/CANVAS/tables/sample_course/770000832960058/discussion_topic_dim.csv', sep=None)
    sub_comment_dim = pd.read_csv(
        '../datasets/CANVAS/tables/sample_course/770000832960058/submission_comment_participant_dim.csv',
        sep=None)
    sub_comment = pd.read_csv('../datasets/CANVAS/tables/sample_course/770000832960058/submission_comment_fact.csv',
                              sep=None)
    enrollment = pd.read_csv('../datasets/CANVAS/tables/sample_course/770000832960058/enrollment_fact.csv', sep=None)
    enrollment_dim = pd.read_csv('../datasets/CANVAS/tables/sample_course/770000832960058/enrollment_dim.csv', sep=None)
    print("activity data imported")
    return quiz_dim,assignment_fact, assignment_dim, sub_a, sub_a_dim, discussion, conversation, wiki \
        , discussion_topic, discussion_dim, conversation_dim, discussion_topic_dim, sub_comment_dim, sub_comment, enrollment, enrollment_dim


def importdata_testing():
    quiz_fact = pd.read_csv('../datasets/CANVAS/tables/quiz_fact.csv', sep=None)
    quiz_dim = pd.read_csv('../datasets/CANVAS/tables/quiz_dim.csv', sep=None)
    sub_q = pd.read_csv('../datasets/CANVAS/tables/for_testing/quiz_submission_fact.csv', sep=None)
    sub_q_dim = pd.read_csv('../datasets/CANVAS/tables/for_testing/quiz_submission_dim.csv', sep=None)

    print("quiz data imported")
    # import assignment data

    assignment_fact = pd.read_csv('../datasets/CANVAS/tables/assignment_fact.csv', sep=None)
    assignment_dim = pd.read_csv('../datasets/CANVAS/tables/assignment_dim.csv', sep=None)
    assignment_dim['assignment_id'] = assignment_dim['id'].tolist()
    sub_a = pd.read_csv('../datasets/CANVAS/tables/for_testing/submission_fact.csv', sep=None)
    sub_a_dim = pd.read_csv('../datasets/CANVAS/tables/for_testing/submission_dim-tdoan.csv', sep=None)
    print("assignment data imported")

    # import activities
    discussion = pd.read_csv('../datasets/CANVAS/tables/for_testing/discussion_entry_fact.csv', sep=None)
    conversation = pd.read_csv('../datasets/CANVAS/tables/for_testing/conversation_message_participant_fact.csv',
                               sep=None)
    wiki = pd.read_csv('../datasets/CANVAS/tables/for_testing/wiki_page_fact.csv', sep=None)
    discussion_topic = pd.read_csv('../datasets/CANVAS/tables/for_testing/discussion_topic_fact.csv', sep=None)
    discussion_dim = pd.read_csv('../datasets/CANVAS/tables/for_testing/discussion_entry_dim.csv', sep=None)
    conversation_dim = pd.read_csv('../datasets/CANVAS/tables/for_testing/conversation_message_dim.csv', sep=None)
    discussion_topic_dim = pd.read_csv('../datasets/CANVAS/tables/for_testing/discussion_topic_dim.csv', sep=None)
    sub_comment_dim = pd.read_csv('../datasets/CANVAS/tables/for_testing/submission_comment_participant_dim.csv',
                                  sep=None)
    sub_comment = pd.read_csv('../datasets/CANVAS/tables/for_testing/submission_comment_fact.csv', sep=None)
    enrollment = pd.read_csv('../datasets/CANVAS/tables/for_testing/enrollment_fact.csv', sep=None)
    print("activity data imported")
    return quiz_fact, quiz_dim, sub_q, sub_q_dim, assignment_fact, assignment_dim, sub_a, sub_a_dim, discussion, conversation, wiki \
        , discussion_topic, discussion_dim, conversation_dim, discussion_topic_dim, sub_comment_dim, sub_comment, enrollment


quiz_dim,assignment_fact, assignment_dim, sub_a, sub_a_dim, discussion, conversation, wiki \
        , discussion_topic, discussion_dim, conversation_dim, discussion_topic_dim, sub_comment_dim, sub_comment, enrollment, enrollment_dim \
    = importdata()

def import_requests(course_id):
    path = os.path.join("..", "datasets", 'CANVAS', 'tables', 'requests_subset_new', str(course_id), 'more_types')
    files_list = [f for f in listdir(path) if isfile(join(path, f)) if f[-3:] == 'csv']
    R = []
    for f in files_list:
        #         print('reading' + str(f))
        r = pd.read_csv(join(path, f))
        # print(r.shape)
        R.append(r)
    R_df = pd.concat(R)
    R_df['timestamp'] = pd.to_datetime(R_df['timestamp'])
    return R_df


def nondropout(course_id, df):
    # if 'course_id' in df.columns.tolist() == False:
    #     df['course_id'] = course_id *len(df)
    # else:
    #     pass
    enrollment_dim.columns = ['enrollment_id'] + enrollment_dim.columns.tolist()[1:]
    ed = enrollment_dim[enrollment_dim['course_id'] == course_id][['user_id', 'type', 'course_id']]
    ef = enrollment[enrollment['course_id'] == course_id]
    e = pd.merge(ef, ed, on=['user_id', 'course_id'], sort=False, how='left')
    e_s = e[e['type'] == 'StudentEnrollment']
    df_stayed = pd.merge(df, e_s[['user_id', 'computed_final_score']], on=['user_id'], sort=False, how='left')
    df_stayed = df_stayed[df_stayed['computed_final_score'] > 0]
    return df_stayed


def create_quiz_sub_time(course_id, sub_q, sub_q_dim, quiz_fact, quiz_dim):
    # create quiz submission time table
    quiz_dim.columns = ['quiz_id'] + quiz_dim.columns.tolist()[1:]
    sub_q_fact_s = sub_q[sub_q['course_id'] == course_id] \
        [['quiz_submission_id', 'quiz_id', 'course_id', 'user_id', 'score', 'quiz_points_possible', 'total_attempts',
          'time_taken']]
    # sub_q_fact_s
    keep_col = ['id', 'quiz_id', 'user_id', 'created_at', 'started_at', 'finished_at', 'due_at']
    sub_q_dim_s = sub_q_dim[sub_q_dim['quiz_id'].isin(quiz_fact[quiz_fact['course_id'] == course_id]['quiz_id'])][
        keep_col]
    sub_q_dim_s.columns = ['quiz_submission_id'] + sub_q_dim_s.columns.tolist()[1:]
    sub_quiz_info = pd.merge(sub_q_fact_s, sub_q_dim_s, on=['quiz_submission_id', 'quiz_id', 'user_id'])
    sub_quiz_info = sub_quiz_info[(sub_quiz_info['due_at'] != '0000-00-00 00:00:00') & \
                                  (sub_quiz_info['started_at'] != '0000-00-00 00:00:00')]
    sub_quiz_info = pd.merge(sub_quiz_info, quiz_dim[['quiz_id', 'created_at',
                                                      'published_at', 'unlock_at']], on='quiz_id', how='left')
    sub_quiz_info.columns = ['quiz_submission_id', 'quiz_id', 'course_id', 'user_id', 'quizsub_score',
                             'quiz_points_possible', 'quizsub_attempts', 'quizsub_time_taken', 'quizsub_created_at',
                             'quizsub_started_at', 'quizsub_finished_at', 'quiz_due_at',
                             'quiz_created_at', 'quiz_published_at', 'quiz_unlock_at']
    for l in ['quizsub_created_at', 'quizsub_started_at', 'quizsub_finished_at', 'quiz_due_at', 'quiz_created_at',
              'quiz_published_at', 'quiz_unlock_at']:
        sub_quiz_info[l] = pd.to_datetime(sub_quiz_info[l])
    q = sub_quiz_info. \
        groupby(['user_id'], sort=False, as_index=False). \
        agg({"quiz_due_at": list, "quizsub_created_at": list})
    return q


def create_assignment_sub_time(course_id,keep_late=True):
    # create assignment submission time table
    assignment_dim['assignment_id'] = assignment_dim['id'].tolist()

    sub_a_fact_s = sub_a[sub_a['course_id'] == course_id] \
        [['submission_id', 'assignment_id', 'course_id', 'user_id', 'score', 'submission_comments_count']].dropna()
    keep_col = ['id', 'submitted_at', 'created_at', 'attempt', 'assignment_id']
    sub_a_dim_s = sub_a_dim[
        sub_a_dim['assignment_id'].isin(assignment_fact[assignment_fact['course_id'] == course_id]['assignment_id'])][
        keep_col].dropna()
    sub_a_dim_s.columns = ['submission_id'] + sub_a_dim_s.columns.tolist()[1:]
    sub_assignment_info = pd.merge(sub_a_fact_s, sub_a_dim_s, on=['submission_id', 'assignment_id'])
    # sub_assignment_info = sub_assignment_info[(sub_assignment_info['due_at']!='0000-00-00 00:00:00')&\
    #                               (sub_assignment_info['started_at']!='0000-00-00 00:00:00')]
    sub_assignment_info = pd.merge(sub_assignment_info, assignment_dim[['assignment_id',
                                                                        'points_possible', 'created_at', 'due_at',
                                                                        'lock_at']],
                                   on='assignment_id').dropna(subset=['due_at'])
    # sub_assignment_info = sub_assignment_info[(sub_assignment_info['due_at']!='0000-00-00 00:00:00')&\
    #                               (sub_assignment_info['started_at']!='0000-00-00 00:00:00')]
    for l in ['created_at_x', 'submitted_at', 'due_at', 'lock_at', 'created_at_y']:
        sub_assignment_info[l] = pd.to_datetime(sub_assignment_info[l])
    cols = ['submission_id',
            'assignment_id',
            'course_id',
            'user_id',
            'assignmentsub_score',
            'submission_comments_count',
            'assignmentsub_submitted_at',
            'assignmentsub_created_at',
            'assignmentsub_attempt',
            'assignment_points_possible',
            'assignment_created_at',
            'assignment_due_at',
            'assignment_lock_at']
    # cols = ['sub_create_at' if x =='created_at_x' else 'created_at' if x == 'created_at_y' else x  for x in cols]
    sub_assignment_info.columns = cols
    is_late = [x > y for x, y in
               zip(sub_assignment_info['assignmentsub_created_at'], sub_assignment_info['assignment_due_at'])]
    sub_assignment_info['is_late'] = is_late
    #     keep_late = True
    if not keep_late:

        nolate = sub_assignment_info[~sub_assignment_info['is_late'] == True]
        # print(nolate.columns)
        a = nolate. \
            groupby(['user_id'], sort=False, as_index=False). \
            agg({"assignment_due_at": list, "assignment_lock_at": list, "assignmentsub_created_at": list,
                 "assignmentsub_submitted_at": list, "is_late": list})
    else:
        a = sub_assignment_info. \
            groupby(['user_id'], sort=False, as_index=False). \
            agg({"assignment_due_at": list, "assignment_lock_at": list, "assignmentsub_created_at": list,
                 "assignmentsub_submitted_at": list, "is_late": list})
    return a


def create_assignment_ind_sub_time(course_id):
    # create assignment submission time table
    assignment_dim['assignment_id'] = assignment_dim['id'].tolist()

    sub_a_fact_s = sub_a[sub_a['course_id'] == course_id] \
        [['submission_id', 'assignment_id', 'course_id', 'user_id', 'score', 'submission_comments_count']].dropna()
    keep_col = ['id', 'submitted_at', 'created_at', 'attempt', 'assignment_id']
    sub_a_dim_s = sub_a_dim[
        sub_a_dim['assignment_id'].isin(assignment_fact[assignment_fact['course_id'] == course_id]['assignment_id'])][
        keep_col].dropna()
    sub_a_dim_s.columns = ['submission_id'] + sub_a_dim_s.columns.tolist()[1:]
    sub_assignment_info = pd.merge(sub_a_fact_s, sub_a_dim_s, on=['submission_id', 'assignment_id'])
    # sub_assignment_info = sub_assignment_info[(sub_assignment_info['due_at']!='0000-00-00 00:00:00')&\
    #                               (sub_assignment_info['started_at']!='0000-00-00 00:00:00')]
    sub_assignment_info = pd.merge(sub_assignment_info, assignment_dim[['assignment_id',
                                                                        'points_possible', 'created_at', 'due_at',
                                                                        'lock_at']],
                                   on='assignment_id').dropna(subset=['due_at'])
    # sub_assignment_info = sub_assignment_info[(sub_assignment_info['due_at']!='0000-00-00 00:00:00')&\
    #                               (sub_assignment_info['started_at']!='0000-00-00 00:00:00')]
    for l in ['created_at_x', 'submitted_at', 'due_at', 'lock_at', 'created_at_y']:
        sub_assignment_info[l] = pd.to_datetime(sub_assignment_info[l])
    cols = ['submission_id',
            'assignment_id',
            'course_id',
            'user_id',
            'assignmentsub_score',
            'submission_comments_count',
            'assignmentsub_submitted_at',
            'assignmentsub_created_at',
            'assignmentsub_attempt',
            'assignment_points_possible',
            'assignment_created_at',
            'assignment_due_at',
            'assignment_lock_at']
    # cols = ['sub_create_at' if x =='created_at_x' else 'created_at' if x == 'created_at_y' else x  for x in cols]
    sub_assignment_info.columns = cols

    ind_a = sub_assignment_info.groupby(['user_id','assignment_id']).agg({"assignmentsub_submitted_at":'first',"assignmentsub_created_at":'first',\
                          'assignment_created_at':'first', 'assignment_due_at':'first'}).reset_index()
    ind_a['is_late'] = [x > y for x, y in zip(ind_a['assignmentsub_submitted_at'].tolist(), ind_a['assignment_due_at'].tolist())]
    return ind_a



def create_discussion_time(course_id):
    if len(discussion_dim) > 0:
        # create discussion time table
        discussion_dim.columns = ['discussion_entry_id'] + discussion_dim.columns.tolist()[1:]
        D = pd.merge(discussion_dim, discussion, on=['discussion_entry_id'])
        D_sel = D[D['course_id'] == course_id][['created_at', 'user_id', 'course_id']]
        D_sel['created_at'] = pd.to_datetime(D_sel['created_at'])

        Dis = D_sel.groupby(['user_id', 'course_id'])['created_at'].apply(list).reset_index()
        Dis.columns = ['user_id', 'course_id', 'created_at_dis']
        Dis = Dis[['user_id', 'created_at_dis']]
    else:
        Dis = pd.DataFrame(columns=['user_id', 'created_at_dis'])
    return Dis


def create_discussion_topic_time(course_id):
    # create discussion topic time table
    if len(discussion_topic) > 0:
        discussion_topic_dim.columns = ['discussion_topic_id'] + discussion_topic_dim.columns.tolist()[1:]
        D_topic = pd.merge(discussion_topic_dim, discussion_topic, on=['discussion_topic_id'])
        D_topic['created_at'] = pd.to_datetime(D_topic['created_at'])

        Dis_topic = D_topic[D_topic['course_id'] == course_id].groupby(['user_id', 'course_id'])['created_at'].apply(
            list).reset_index()
        Dis_topic.columns = ['user_id', 'course_id', 'created_at_topic']
        Dis_topic = Dis_topic[['user_id', 'created_at_topic']]
    else:
        Dis_topic = pd.DataFrame(columns=['user_id', 'created_at_topic'])
    return Dis_topic


def create_conversation_time(course_id):
    # create conversation time table
    col = ['user_id' if x == 'author_id' else x for x in conversation_dim.columns]
    conversation_dim.columns = col
    conversation_dim.columns = ['conversation_message_id'] + conversation_dim.columns.tolist()[1:]
    C = pd.merge(conversation_dim, conversation, on=['conversation_message_id', 'user_id', 'conversation_id'])
    C_sel = C[C['course_id'] == course_id][['created_at', 'user_id', 'course_id']]
    C_sel['created_at'] = pd.to_datetime(C_sel['created_at'])
    Conv = C_sel.groupby(['user_id', 'course_id'])['created_at'].apply(list).reset_index()
    if len(Conv) > 0:
        Conv.columns = ['user_id', 'course_id', 'created_at_msg']
        Conv = Conv[['user_id', 'created_at_msg']]
    else:
        Conv = pd.DataFrame(columns=['user_id', 'created_at_msg'])
    return Conv


def create_comment_time(course_id):
    # create assignment submission comments time table
    col = ['user_id' if x == 'author_id' else x for x in sub_comment.columns]
    sub_comment.columns = col
    sub_comment_dim.columns = ['submission_comment_id'] + sub_comment_dim.columns.tolist()[1:]
    Cmt = pd.merge(sub_comment_dim, sub_comment, on=['submission_comment_id'])
    Cmt['created_at'] = pd.to_datetime(Cmt['created_at'])
    Comment = Cmt[Cmt['course_id'] == course_id].groupby(['user_id', 'course_id']) \
        ['created_at'].apply(list).reset_index()
    if len(Comment) > 0:
        Comment.columns = ['user_id', 'course_id', 'created_at_comment']
        Comment = Comment[['user_id', 'created_at_comment']]
    else:
        Comment = pd.DataFrame(columns=['user_id', 'created_at_comment'])
    return Comment


def create_requests_time(course_id):
    # create time tables for different activities extracted from requests.
    R_df = import_requests(course_id)
    R = nondropout(course_id, R_df)
    R_q = R[(~R['quiz_id'].isna()) | (
        R['web_application_controller'].isin(['quizzes/quizzes', 'quizzes/quizzes_submissions']))] \
        [['user_id', 'quiz_id', 'timestamp']].groupby(['user_id', 'quiz_id'])['timestamp'].apply(list).reset_index()
    R_q.columns = ['user_id', 'quiz_id', 'timestamp']

    R_a = R[(~R['assignment_id'].isna()) | (
        R['web_application_controller'].isin(['assignments', 'assignments_api', 'submissions', 'submissions_api']))] \
        [['user_id', 'assignment_id', 'timestamp']].groupby(['user_id', 'assignment_id'])['timestamp'].apply(
        list).reset_index()
    # R_dis_entry = R[['user_id', 'timestamp', 'discussion_id']].dropna(subset=['discussion_id'])
    #
    # R_dis_topic = R[R['web_application_controller'].isin(['discussion_topics', 'discussion_topics_api'])][['user_id' \
    #     , 'timestamp', 'web_application_controller']]
    # R_dis_topic.columns = ['user_id', 'timestamp', 'discussion_id']
    #
    # R_dis = pd.concat([R_dis_entry, R_dis_topic]).groupby(['user_id'])['timestamp'].apply(list).reset_index()
    # R_dis.columns = ['user_id', 'dis_r']
    R_d = R[(~R['discussion_id'].isna()) | (
        R['web_application_controller'].isin(['discussion_entries', 'discussion_topics', 'discussion_topics_api']))] \
        [['user_id', 'timestamp']].groupby(['user_id'])['timestamp'].apply(list).reset_index()
    R_d.columns = ['user_id', 'dis_r']

    R_module = \
        R[(~R['wiki_page_id'].isna()) | (R['web_application_controller'].isin(['wiki_page', 'wiki_page_api', 'files']))] \
            [['user_id', 'timestamp']].groupby(['user_id'])['timestamp'].apply(list).reset_index()
    R_module.columns = ['user_id', 'module_r']

    R_conv = R[['user_id', 'timestamp', 'conversation_id']].dropna(subset=['conversation_id']). \
        groupby(['user_id'])['timestamp'].apply(list).reset_index()
    R_conv.columns = ['user_id', 'conv_r']

    return R_q, R_a, R_d, R_module, R_conv


def agg_assignment_time(course_id,R_a,R_q):
    ind_a = create_assignment_ind_sub_time(course_id)
    ma = pd.merge(ind_a, R_a, on=['user_id', 'assignment_id'], how='left')
    ma['timestamp'] = ma['timestamp'].apply(lambda d: d if isinstance(d, list) else [])
    ma['all'] = [[x] + [y] + z for x, y, z in zip(ma['assignmentsub_submitted_at'].tolist(),ma['assignmentsub_created_at'].tolist(),
                                                  ma['timestamp'].tolist())]
    ma = ma[['user_id', 'assignment_id', 'assignment_due_at', 'all']]
    ma['act_count'] = [len(x) for x in ma['all'].tolist()]
    R_q = pd.merge(R_q, quiz_dim[['quiz_id', 'assignment_id']], on='quiz_id', how='left')
    R_sub = pd.merge(R_q, R_a, on=['user_id', 'assignment_id'], how='outer')
    R_sub['timestamp_x'] = R_sub['timestamp_x'].apply(lambda d: d if isinstance(d, list) else [])
    R_sub['timestamp_y'] = R_sub['timestamp_y'].apply(lambda d: d if isinstance(d, list) else [])

    R_sub['timestamp'] = [x + y for x, y in zip(R_sub['timestamp_x'].tolist(), R_sub['timestamp_y'].tolist())]
    R_sub = R_sub[['user_id', 'assignment_id', 'timestamp']]
    merged_sub = pd.merge(ind_a, R_sub, on=['user_id', 'assignment_id'], how='left')
    merged_sub['timestamp'] = merged_sub['timestamp'].apply(lambda d: d if isinstance(d, list) else [])
    merged_sub['all'] = np.array([[x] + [y] + z for x, y, z in zip(merged_sub['assignmentsub_submitted_at'].tolist(),\
                                                                   merged_sub['assignmentsub_created_at'].tolist(), \
                                                                   merged_sub['timestamp'].tolist())]).flatten()
    merged_sub['act_count'] = [len(list(set(x))) for x in merged_sub['all'].tolist()]
    merged_sub['start_time'] = [min(x) for x in merged_sub['all']]
    merged_sub['end_time'] = [max(x) for x in merged_sub['all']]

    return merged_sub


def agg_time(R_a, a, R_q, Dis, Dis_topic, R_dis, Comment, Conv, R_conv, R_module, Dimensions, course_id, enrollment,
             enrollment_dim, k, deadline_method):
    '''

    :param R_a:
    :param a:
    :param R_q:
    :param q:
    :param Dis:
    :param Dis_topic:
    :param R_dis:
    :param Comment:
    :param Conv:
    :param R_conv:
    :param R_wiki:
    :param agg_lists:
    :param Dimensions: dictionary with key - dimension name, and values = lists
    :return:
    '''
    from functools import reduce
    All_merge = reduce(lambda left, right: pd.merge(left, right, on=['user_id'],
                                                    how='outer'),
                       [a, R_a, R_q, Dis, Dis_topic, R_dis, Comment, Conv, R_conv, R_module])
    for c in All_merge.columns.tolist()[1:]:
        All_merge[c] = All_merge[c].apply(lambda d: d if isinstance(d, list) else [])
    All_merge = nondropout(course_id, All_merge)
    agg_merge = pd.DataFrame()
    if Dimensions == 'default':
        A_list = ['assignment_r',
                  'quiz_r',
                  #                   'assignment_due_at',
                  'assignmentsub_submitted_at',
                  'assignmentsub_created_at']
        # Q_list = ['quiz_r',
        #           'quiz_due_at',
        #           'quizsub_created_at']
        C_list = ['created_at_dis',
                  'created_at_topic',
                  'dis_r',
                  'created_at_comment',
                  'created_at_msg',
                  'conv_r']
        W_list = ['module_r']
        D_list_a = [deadline_method]
        # D_list_q = ['quiz_due_at']
        agg_lists = [D_list_a, A_list, C_list, W_list]
        column_names = ['Deadline', 'Assignment_agg', 'Communication_agg',
                        'Module_agg']
        Dimensions = dict(zip(column_names, agg_lists))
    else:
        pass
    for l in list(Dimensions.values()):
        t = All_merge[l]
        agg_merge[str(l)] = [sum(x, []) for x in t.values.tolist()]
    agg_merge['user_id'] = All_merge['user_id'].tolist()
    # agg_merge.columns = ['Deadline_agg_a','Deadline_agg_q','Assignment_agg','Quiz_agg','Communication_agg',
    # 'Wiki_agg','user_id']
    agg_merge.columns = list(Dimensions.keys()) + ['user_id']
    """only keep students who have no less than k submissions """
    #     agg_merge['subcount'] = [len(x) for x in agg_merge['Deadline'].tolist()]
    if deadline_method == 'assignment_lock_at':
        agg_merge['subcount'] = [len(x) for x in All_merge['is_late']]
    elif deadline_method == 'assignment_due_at':
        agg_merge['subcount'] = [x.count(False) for x in All_merge['is_late']]
    agg_merge_kept = agg_merge[agg_merge['subcount'] >= k]
    return agg_merge_kept


def time2timestamp(df):
    """
    :param df:
    :param columns:
    :param course_id:
    :param enrollment:
    :return:
    """

    import time
    new_df = pd.DataFrame()
    for c in df.columns:
        timelist = df[c].tolist()
        if c not in ['user_id', 'subcount']:
            unixtimelist = [sorted([time.mktime(xx.timetuple()) / 3600 for xx in x], reverse=True) for x in timelist]
            new_df[c + str('_timestamp')] = unixtimelist
        else:
            new_df[c] = df[c].tolist()
    #             print('non time type: ' +str(c))
    # new = nondropout(course_id, new_df, enrollment,enrollment_dim)
    # new = new[new['sub_count'] > 0]
    return new_df


def pre_hawkess(df=None, course_id=None, flavor=None, assignment_dim=None, deadlines_name=None):
    # todo: late submissions timestamps
    import time
    """
    :param df: aggregated time stamp table
    :param flavor: flavor to preprocess data, could be 'all_ddls' or 'sub_ddls' or other
    :param deadlines_name: the column names that point to deadlines
    """

    if flavor == 'all_ddls':
        ## use all submission deadlines as one dimension, last deadline of the course = 0
        pre_df = df
        assignment_all_ddls = pd.to_datetime(
            assignment_dim[assignment_dim['course_id'] == course_id].dropna(subset=['lock_at'])['due_at']).tolist()
        assignment_all_ddls_timestamp = sorted([time.mktime(x.timetuple()) / 3600 for x in assignment_all_ddls])

        last_ddl = np.max(assignment_all_ddls_timestamp)
        pre_df = df.drop(columns=deadlines_name)
        pre_df['Deadline_timestamp'] = [sorted(assignment_all_ddls_timestamp, reverse=True)] * len(df)
        # pre_df['quiz_all_ddls_timestamp'] = [sorted(quiz_all_ddls_timestamp, reverse=True)] * len(df)
        # print(quiz_all_ddls_timestamp)
        for c in pre_df.columns.tolist():
            # print(len(df.dropna(subset = [c])[c]))
            if c not in ['user_id', 'computed_final_score']:
                try:
                    pre_df[c] = [[last_ddl - xx for xx in x] for x in pre_df[c].tolist()]
                except:
                    print(c)
            else:
                pass

    elif flavor == 'sub_ddls':
        # use only the deadlines of submitted work as one dimension, last individual submission deadline = 0
        pre_df = df
        if len(deadlines_name) > 1:
            last_ddl = [np.max(list(x) + list(y)) for x, y in
                        zip(df['Deadline_agg_a_timestamp'].tolist(), df['Deadline_agg_q_timestamp'].tolist())]
        else:
            last_ddl = [np.max(x) for x in df[deadlines_name[0]].tolist()]
        # print('last ddl: ' + str(last_ddl))

        for c in df.columns.tolist():
            if c not in ['user_id', 'computed_final_score', 'subcount']:
                try:
                    pre_df[c] = [x - y for x, y in zip(last_ddl, df[c].tolist())]
                except:
                    pass
            else:
                pass

    elif flavor == 'other':
        # use the last deadline in the course as 0
        assignment_all_ddls = pd.to_datetime(
            assignment_dim[assignment_dim['course_id'] == course_id].dropna(subset=['lock_at'])['due_at']).tolist()
        assignment_all_ddls_timestamp = sorted([time.mktime(x.timetuple()) / 3600 for x in assignment_all_ddls])
        # """course_id in quiz_fim is wrong so use the following way to extract ddls"""
        # quiz_all_ddls = pd.to_datetime(
        #     quiz_dim[quiz_dim['quiz_id'].isin(quiz_fact[quiz_fact['course_id'] == course_id]['quiz_id']. \
        #                                       tolist())].dropna(subset=['lock_at'])['due_at']).tolist()
        # quiz_all_ddls_timestamp = sorted([time.mktime(x.timetuple()) / 3600 for x in quiz_all_ddls])

        last_ddl = np.max(list(assignment_all_ddls_timestamp))
        # print('last ddl: ' + str(last_ddl))
        pre_df = df
        for c in df.columns.tolist():
            if c not in ['user_id', 'computed_final_score']:
                pre_df[c] = [last_ddl - y for y in df[c].tolist()]

            else:
                pass
    return pre_df


def student_grade(sub_a, assignment_fact, course_id, enrollment, enrollment_dim):
    sub_a_s = sub_a[sub_a['course_id'] == course_id]
    sub_a_s = nondropout(course_id, sub_a_s, enrollment, enrollment_dim).dropna(subset=['score'])
    sub_a_sel = pd.merge(sub_a_s, assignment_fact[['assignment_id', 'points_possible']], sort=False,
                         on=['assignment_id'], how='left')
    sub_a_sel = sub_a_sel[sub_a_sel['points_possible'] > 0]
    assignment_grade = sub_a_sel.groupby(['user_id'], sort=False).agg(
        {'assignment_id': list, 'score': list, 'points_possible': list})
    assignment_grade['avg_norm_a'] = [np.mean([i / j for i, j in zip(x, y)]) for x, y in
                                      zip(assignment_grade['score'].tolist(),
                                          assignment_grade['points_possible'].tolist())]
    assignment_grade['weighted_avg_norm_a'] = [np.sum(x) / np.sum(y) for x, y in
                                               zip(assignment_grade['score'].tolist(),
                                                   assignment_grade['points_possible'].tolist())]
    weighted_a = assignment_grade.reset_index()[['user_id', 'weighted_avg_norm_a']]
    return weighted_a
