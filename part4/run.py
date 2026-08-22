from flask import Flask, render_template

# هنا نخبر فلاسك أن يبحث عن القوالب والملفات الثابتة داخل مجلد app
app = Flask(__name__, template_folder='app/templates', static_folder='app/static')

# هذا هو المسار الرئيسي للصفحة
@app.route('/')
def login_page():
    return render_template('index.html')

if __name__ == '__main__':
    # تفعيل الـ debug ممتاز أثناء التطوير ليتم تحديث التعديلات تلقائياً
    app.run(debug=True)