from Hawkes.utils import *
import tick
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from tick.hawkes import HawkesADM4, HawkesExpKern
import os


def model_hawkes(df=None, learnertype=None, decay=None, Dimensions=None,flavor = None,def_low=None ,def_high=None):
    path = os.path.join(os.getcwd())
    n_nodes = len(list(Dimensions.keys()))
    df = df.dropna(subset = ['computed_final_score'])
    if learnertype == 'HawkesExpKern':
        try:
            p = os.path.join(path, 'results', 'tables', learnertype,flavor, str(n_nodes) + '_nodes')
            p1 = os.path.join(path, 'results', 'figs', learnertype, flavor, str(n_nodes) + '_nodes')
            print(p)
            os.makedirs(p)
            os.makedirs(p1)
        except FileExistsError:
            print('folders exist')
        else:
            print('created.')

        for d in decay:
            A = []
            B = []
            learner = HawkesExpKern(decays=d)
            for i in range(len(df)):
                s1 = df.iloc[i, :len(Dimensions.keys())].tolist()
                learner.fit(s1)
                A.append(learner.adjacency)
                B.append(learner.baseline)
            A_super = pd.DataFrame([list(x) for x in A])
            A_super.columns = list(Dimensions.keys())
            A_super['user_id'] = df['user_id'].tolist()
            A_super['computed_final_score'] = df['computed_final_score'].tolist()
            B_super = pd.DataFrame(list(x) for x in B)
            B_super.columns = list(Dimensions.keys())
            B_super['user_id'] = df['user_id'].tolist()
            B_super['computed_final_score'] = df['computed_final_score'].tolist()
            A_super.to_csv(p + '/A_' + str(d) + '.csv',
                           index=False)
            B_super.to_csv(p + '/B_' + str(d) + '.csv',
                           index=False)
            score = A_super['computed_final_score'].tolist()
            plot_hawkes(n_nodes, A_super, B_super, learnertype, d, score, Dimensions, p1,def_low,def_high)

    elif learnertype == 'HawkesADM4':
        try:
            p = os.path.join(path, 'results', 'tables', learnertype,flavor, str(n_nodes) + '_nodes')
            p1 = os.path.join(path, 'results', 'figs', learnertype, flavor, str(n_nodes) + '_nodes')
            os.makedirs(p)
            os.makedirs(p1)
        except FileExistsError:
            pass
        else:
            print('folders created')

        for d in decay:
            A = []
            B = []
            learner = HawkesADM4(decay=d)
            for i in range(len(df)):
                s1 = df.iloc[i, :len(Dimensions.keys())].tolist()
                learner.fit(s1)
                A.append(learner.adjacency)
                B.append(learner.baseline)
            A_super = pd.DataFrame([list(x) for x in A])
            A_super.columns = list(Dimensions.keys())
            A_super['user_id'] = df['user_id'].tolist()
            A_super['computed_final_score'] = df['computed_final_score'].tolist()
            B_super = pd.DataFrame(list(x) for x in B)
            B_super.columns = list(Dimensions.keys())
            B_super['user_id'] = df['user_id'].tolist()
            B_super['computed_final_score'] = df['computed_final_score'].tolist()
            A_super.to_csv(p + '/A_' + str(d) + '.csv',
                           index=False)
            B_super.to_csv(p + '/B_' + str(d) + '.csv',
                           index=False)
            score = A_super['computed_final_score'].tolist()
            plot_hawkes(n_nodes, A_super, B_super, learnertype, d, score, Dimensions, p1,def_low,def_high)
    else:
        print('function not implemented.')


def plot_hawkes(n_nodes, A_super, B_super, learnertype, d, score, Dimensions, p1,def_low,def_high ):
    low_q = np.quantile(score,def_low)
    high_q = np.quantile(score,def_high)
    A_high = A_super[A_super['computed_final_score']>=high_q]
    A_low  = A_super[A_super['computed_final_score']<low_q]
    B_high = B_super[B_super['computed_final_score']>=high_q]
    B_low = B_super[B_super['computed_final_score']<low_q]

    if n_nodes == 3:
        for c in list(Dimensions.keys())[1:]:
            plt.figure()
            plt.title(str(learnertype) + ',decay = ' + str(d) + 'h')
            plt.scatter(score, B_super[c].tolist(),s = 3)
            plt.ylabel('base intensity_' + c)
            plt.xlabel('computed final score')
            plt.title(str(learnertype) + ',decay = ' + str(d) + 'h')
            plt.savefig(p1 + '/B_' + str(c) +"_"+str(d) + '.png')
            plt.close()

            plt.figure()
            plt.title(str(learnertype) + ',decay = ' + str(d) + 'h')
            sns.distplot(B_high[c],label='high')
            sns.distplot(B_low[c],label='low')
            plt.legend()
            plt.xlabel('base intensity_' + c)
            plt.savefig(p1 + '/B_' + str(c) + "_" + str(d) + '_distplot.png')
            plt.close()



        D2S = np.array(A_super.iloc[:, 1].tolist())[:, 0]
        D2A = np.array(A_super.iloc[:, 2].tolist())[:, 0]
        S2A = np.array(A_super.iloc[:, 2].tolist())[:, 1]
        A2S = np.array(A_super.iloc[:, 1].tolist())[:, 2]
        S2S = np.array(A_super.iloc[:, 2].tolist())[:, 2]
        A2A = np.array(A_super.iloc[:, 1].tolist())[:, 1]

        plt.figure(figsize=(10, 10))

        plt.subplot(321)
        plt.scatter(score, D2S)
        plt.xlabel('computed_final_score')
        plt.ylabel('deadline2submission')

        plt.subplot(322)
        plt.scatter(score, D2A)
        plt.xlabel('computed_final_score')
        plt.ylabel('deadline2activity')

        plt.subplot(323)
        plt.scatter(score, S2A)
        plt.xlabel('computed_final_score')
        plt.ylabel('submission2activity')

        plt.subplot(324)
        plt.scatter(score, A2S)
        plt.xlabel('computed_final_score')
        plt.ylabel('activity2submission')

        plt.subplot(325)
        plt.scatter(score, S2S)
        plt.xlabel('computed_final_score')
        plt.ylabel('submission2submission')

        plt.subplot(326)
        plt.scatter(score, A2A)
        plt.xlabel('computed_final_score')
        plt.ylabel('activity2activity')


        plt.legend()

        plt.subplots_adjust(top=0.92, bottom=0.1, left=0.10, right=0.95, hspace=0.35,
                            wspace=0.35)
        plt.savefig(p1 + '/A_' + str(d) + '.png')
        plt.close()


        plt.figure(figsize=(10, 10))
        D2Shigh = np.array(A_high.iloc[:, 1].tolist())[:, 0]
        D2Ahigh = np.array(A_high.iloc[:, 2].tolist())[:, 0]
        S2Ahigh = np.array(A_high.iloc[:, 2].tolist())[:, 1]
        A2Shigh = np.array(A_high.iloc[:, 1].tolist())[:, 2]
        A2Ahigh = np.array(A_high.iloc[:, 1].tolist())[:, 1]
        S2Shigh = np.array(A_high.iloc[:, 2].tolist())[:, 2]

        D2Slow = np.array(A_low.iloc[:, 1].tolist())[:, 0]
        D2Alow = np.array(A_low.iloc[:, 2].tolist())[:, 0]
        S2Alow = np.array(A_low.iloc[:, 2].tolist())[:, 1]
        A2Slow = np.array(A_low.iloc[:, 1].tolist())[:, 2]
        A2Alow = np.array(A_low.iloc[:, 1].tolist())[:, 1]
        S2Slow = np.array(A_low.iloc[:, 2].tolist())[:, 2]

        plt.subplot(321)
        sns.distplot(D2Shigh,hist=False,rug=True,label = 'high')
        sns.distplot(D2Slow,hist=False,rug=True,label = 'low')
        plt.xlabel('deadline2submission')

        plt.subplot(322)
        sns.distplot(D2Ahigh, hist=False,label='high')
        sns.distplot(D2Alow,hist=False, label='low')
        plt.xlabel('deadline2activity')

        plt.subplot(323)
        sns.distplot(S2Ahigh,hist=False, label='high')
        sns.distplot(S2Alow, hist=False,label='low')
        plt.xlabel('submission2activity')

        plt.subplot(324)
        sns.distplot(A2Shigh,hist=False, label='high')
        sns.distplot(A2Slow,hist=False, label='low')
        plt.xlabel('activity2submission')

        plt.subplot(325)
        sns.distplot(S2Shigh, hist=False,label='high')
        sns.distplot(S2Slow,hist=False, label='low')
        plt.xlabel('submission2submission')

        plt.subplot(326)
        sns.distplot(A2Ahigh,hist=False, label='high')
        sns.distplot(A2Alow, hist=False,label='low')
        plt.xlabel('activity2activity')

        plt.legend()

        plt.subplots_adjust(top=0.92, bottom=0.1, left=0.10, right=0.95, hspace=0.35,
                            wspace=0.35)
        plt.savefig(p1 + '/A_' + str(d) + '_dist.png')

        plt.close()

    elif n_nodes == 6:

        for c in list(Dimensions.keys())[2:]:
            plt.figure()
            plt.title(str(learnertype) + ',decay = ' + str(d) + 'h')
            plt.scatter(score, B_super[c].tolist(),s = 3)
            plt.ylabel('base intensity_' + c)
            plt.xlabel('computed final score')
            plt.title(str(learnertype) + ',decay = ' + str(d) + 'h')
            plt.savefig(p1 + '/B_' + str(c) +"_"+str(d) + '.png')
            plt.close()

            plt.figure()
            plt.title(str(learnertype) + ',decay = ' + str(d) + 'h')
            sns.distplot(B_high[c],label='high')
            sns.distplot(B_low[c],label='low')
            plt.legend()
            plt.xlabel('base intensity_' + c)
            plt.savefig(p1 + '/B_' + str(c) + "_" + str(d) + '_distplot.png')
            plt.close()


        DA2A = np.array(A_super.iloc[:, 2].tolist())[:, 0]
        DA2C = np.array(A_super.iloc[:, 4].tolist())[:, 0]
        DA2W = np.array(A_super.iloc[:, 5].tolist())[:, 0]

        DQ2Q = np.array(A_super.iloc[:, 3].tolist())[:, 1]
        DQ2C = np.array(A_super.iloc[:, 4].tolist())[:, 1]
        DQ2W = np.array(A_super.iloc[:, 5].tolist())[:, 1]

        A2C = np.array(A_super.iloc[:, 4].tolist())[:, 2]
        A2W = np.array(A_super.iloc[:, 5].tolist())[:, 2]

        Q2C = np.array(A_super.iloc[:, 4].tolist())[:, 3]
        Q2W = np.array(A_super.iloc[:, 4].tolist())[:, 3]

        C2A = np.array(A_super.iloc[:, 2].tolist())[:, 4]
        C2Q = np.array(A_super.iloc[:, 3].tolist())[:, 4]
        C2W = np.array(A_super.iloc[:, 5].tolist())[:, 4]

        W2A = np.array(A_super.iloc[:, 2].tolist())[:, 5]
        W2Q = np.array(A_super.iloc[:, 3].tolist())[:, 5]
        W2C = np.array(A_super.iloc[:, 4].tolist())[:, 5]

        plt.figure(figsize=(16, 16))

        plt.subplot(421)
        plt.scatter(score, DA2A, s=1.5)
        plt.ylabel('DA2A')
        plt.subplot(422)
        plt.scatter(score, DA2C, s=1.5)
        plt.ylabel('DA2C')

        plt.subplot(423)
        plt.scatter(score, DA2W, s=1.5)
        plt.ylabel('DA2C')

        plt.subplot(424)
        plt.scatter(score, DQ2Q, s=1.5)
        plt.ylabel('DA2W')

        plt.subplot(425)
        plt.scatter(score, DQ2C, s=1.5)
        plt.ylabel('DQ2C')

        plt.subplot(426)
        plt.scatter(score, DQ2W, s=1.5)
        plt.ylabel('DQ2W')

        plt.subplot(427)
        plt.scatter(score, A2C, s=1.5)
        plt.ylabel('A2C')

        plt.subplot(428)
        plt.scatter(score, A2W, s=1.5)
        plt.ylabel('A2W')
        plt.subplots_adjust(top=0.92, bottom=0.1, left=0.10, right=0.95, hspace=0.35,
                            wspace=0.35)
        plt.savefig(p1 + '/A_' + str(d) + '_part1.png')
        plt.close()

        plt.figure(figsize=(16, 16))
        plt.subplot(421)

        plt.scatter(score, Q2C, s=1.5)
        plt.ylabel('Q2C')

        plt.subplot(422)
        plt.scatter(score, Q2W, s=1.5)
        plt.ylabel('Q2W')

        plt.subplot(423)
        plt.scatter(score, C2A, s=1.5)
        plt.ylabel('C2A')

        plt.subplot(424)
        plt.scatter(score, C2Q, s=1.5)
        plt.ylabel('C2Q')

        plt.subplot(425)
        plt.ylabel('C2W')
        plt.scatter(score, C2W, s=1.5)

        plt.subplot(426)
        plt.ylabel('W2A')
        plt.scatter(score, W2A, s=1.5)

        plt.subplot(427)
        plt.ylabel('W2Q')
        plt.scatter(score, W2Q, s=1.5)

        plt.subplot(428)
        plt.ylabel('W2C')
        plt.scatter(score, W2C, s=1.5)
        plt.subplots_adjust(top=0.92, bottom=0.1, left=0.10, right=0.95, hspace=0.35,
                            wspace=0.35)
        plt.savefig(p1 + '/A_' + str(d) + '_part2.png')
        plt.close()
        print('processed: ' + learnertype + "with decay = " + str(d))
    return


