#%%
import pandas as pd
from sklearn import metrics

#%%
def metrics_report(ytrain_true, ytrain_pred_prob, ytest_true, ytest_pred_prob, model, threshold=0.5):
    # gera um relatorio com metricas de qualidade prontas para logar no mlflow ou salvar onde desejar

    ytrain_pred = (ytrain_pred_prob >= threshold).astype(int)
    ytest_pred = (ytest_pred_prob >= threshold).astype(int)

    # df_results = pd.DataFrame(model.cv_results_) # como no optuna so calcula o mean_test_score resolvi nao extrair 
    # best_index = model.best_index_

    report = {'precision_train': round(metrics.precision_score(ytrain_true, ytrain_pred), 3),
              'precision_test': round(metrics.precision_score(ytest_true, ytest_pred), 3),
              
              'recall_train': round(metrics.recall_score(ytrain_true, ytrain_pred), 3),
              'recall_test': round(metrics.recall_score(ytest_true, ytest_pred), 3),

              'f1_train': round(metrics.f1_score(ytrain_true, ytrain_pred), 3),
              'f1_test': round(metrics.f1_score(ytest_true, ytest_pred), 3),
              
              'roc_auc_train': round(metrics.roc_auc_score(ytrain_true, ytrain_pred_prob), 3),
              'roc_auc_test': round(metrics.roc_auc_score(ytest_true, ytest_pred_prob), 3),

              'pr_auc_train': round(metrics.average_precision_score(ytrain_true, ytrain_pred_prob), 3),
              'pr_auc_test': round(metrics.average_precision_score(ytest_true, ytest_pred_prob), 3)
                                                                      
              #'mean_train_score': df_results.loc[best_index, 'mean_train_score'], # essas metricas nao sao calculadas no optuna, apenas o mean_test_score é calculado 
              #'mean_test_score': df_results.loc[best_index, 'mean_test_score'],
              #'std_train_score': df_results.loc[best_index, 'std_train_score'],
              #'std_test_score': df_results.loc[best_index, 'std_test_score']
              }
    
    return report