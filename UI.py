import tkinter as tk
from tkinter import ttk
import pickle


def predict_job(user_skills):
    with open('models.pkl', 'rb') as file:
        models = pickle.load(file)
    svm_clf, rf_clf, dt_clf, nb_clf, lg_clf, tfidf_vectorizer = models

    skills_vector = tfidf_vectorizer.transform([user_skills])
    svm_pred = svm_clf.predict(skills_vector)
    rf_pred = rf_clf.predict(skills_vector)
    dt_pred = dt_clf.predict(skills_vector)
    nb_pred = nb_clf.predict(skills_vector)
    lg_pred = lg_clf.predict(skills_vector)
    predictions = {
        '支持向量机': svm_pred.item(),
        '随机森林': rf_pred.item(),
        '决策树': dt_pred.item(),
        '朴素贝叶斯': nb_pred.item(),
        '逻辑斯谛': lg_pred.item()
    }
    return predictions


def on_submit():
    user_input = entry.get()
    try:
        job=list(predict_job(user_input).items())
    except Exception as e:
        output_text.set(e)
        return
    output_text.set(f'您输入的技能是：\n'
                    f'{user_input}\n\n'
                    f'各个模型推荐的职位为：\n'
                    f'{job[0][0]}：{job[0][1]}\n'
                    f'{job[1][0]}：{job[1][1]}\n'
                    f'{job[2][0]}：{job[2][1]}\n'
                    f'{job[3][0]}：{job[3][1]}\n'
                    f'{job[4][0]}：{job[4][1]}\n')
    entry.delete(0, 'end')


def label_place(event=None):
    window_width = root.winfo_width()
    window_height = root.winfo_height()
    label.place(x=window_width - label.winfo_reqwidth(), y=window_height - label.winfo_reqheight())


root = tk.Tk()
root.title('职位推荐')
root.geometry('500x400')

# 输入框
entry = ttk.Entry(root, width=50, font=('宋体', 16))
entry.pack(padx=20, pady=20)
# 提交按钮
submit_button = tk.Button(root, text='提交', command=on_submit, font=('宋体', 16))
submit_button.pack(pady=10)
# 输出文本
output_text = tk.StringVar()
output_label = ttk.Label(root, textvariable=output_text, foreground='black', font=('宋体', 16))
output_label.pack(padx=20, pady=20)

label = tk.Label(root, text='designed by nzh')
label_place()
root.bind("<Configure>", label_place)

root.mainloop()
