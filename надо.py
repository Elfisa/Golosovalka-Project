import datetime as dt

print(dt.datetime.now() > dt.datetime(2022, 4, 10, 1, 32, 37, 960856))

# if form.short_answer.data:
#     return redirect(url_for('add_question_short_answer'))
# if form.radio_answer.data:
#     return redirect(url_for('add_question_radio_answer'))

# flex-column self-align-center justify-content-center vh-100
# w-100 mx-auto


# {% if current_user.is_authenticated and current_user == vote.author %}
# <div class="row my-2">
#     <a href="/vote_detail/{{ vote.id }}" class="btn" style="background-color: #9ACD32">
#         Изменить
#     </a>
#     <a href="/delete/{{ vote.id }}" class="btn btn-warning">
#         Удалить
#     </a>
# </div>