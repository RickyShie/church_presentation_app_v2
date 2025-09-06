from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectMultipleField, SelectField, SubmitField, TextAreaField, URLField
from wtforms.validators import DataRequired, NumberRange
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.validators import ValidationError

bible_book_choices = [
    ("GEN", "創世記"),
    ("EXO", "出埃及記"),
    ("LEV", "利未記"),
    ("NUM", "民數記"),
    ("DEU", "申命記"),
    ("JOS", "約書亞記"),
    ("JDG", "士師記"),
    ("RUT", "路得記"),
    ("1SA", "撒母耳記上"),
    ("2SA", "撒母耳記下"),
    ("1KI", "列王紀上"),
    ("2KI", "列王紀下"),
    ("1CH", "歷代志上"),
    ("2CH", "歷代志下"),
    ("EZR", "以斯拉記"),
    ("NEH", "尼希米記"),
    ("EST", "以斯帖記"),
    ("JOB", "約伯記"),
    ("PSA", "詩篇"),
    ("PRO", "箴言"),
    ("ECC", "傳道書"),
    ("SNG", "雅歌"),
    ("ISA", "以賽亞書"),
    ("JER", "耶利米書"),
    ("LAM", "耶利米哀歌"),
    ("EZK", "以西結書"),
    ("DAN", "但以理書"),
    ("HOS", "何西阿書"),
    ("JOL", "約珥書"),
    ("AMO", "阿摩司書"),
    ("OBA", "俄巴底亞書"),
    ("JON", "約拿書"),
    ("MIC", "彌迦書"),
    ("NAM", "那鴻書"),
    ("HAB", "哈巴谷書"),
    ("ZEP", "西番雅書"),
    ("HAG", "哈該書"),
    ("ZEC", "撒迦利亞書"),
    ("MAL", "瑪拉基書"),
    ("MAT", "馬太福音"),
    ("MRK", "馬可福音"),
    ("LUK", "路加福音"),
    ("JHN", "約翰福音"),
    ("ACT", "使徒行傳"),
    ("ROM", "羅馬書"),
    ("1CO", "哥林多前書"),
    ("2CO", "哥林多後書"),
    ("GAL", "加拉太書"),
    ("EPH", "以弗所書"),
    ("PHP", "腓立比書"),
    ("COL", "歌羅西書"),
    ("1TH", "帖撒羅尼迦前書"),
    ("2TH", "帖撒羅尼迦後書"),
    ("1TI", "提摩太前書"),
    ("2TI", "提摩太後書"),
    ("TIT", "提多書"),
    ("PHM", "腓利門書"),
    ("HEB", "希伯來書"),
    ("JAS", "雅各書"),
    ("1PE", "彼得前書"),
    ("2PE", "彼得後書"),
    ("1JN", "約翰一書"),
    ("2JN", "約翰二書"),
    ("3JN", "約翰三書"),
    ("JUD", "猶大書"),
    ("REV", "啟示錄"),
]

def AtLeastOneSelected(form, field):
    if not field.data or len(field.data) == 0:
        raise ValidationError("You must select at least one option.")

def google_slides_embed_only(form, field):
    value = (field.data or "").strip()
    # Allow users to paste the whole <iframe> snippet; extract src if present
    import re
    m = re.search(r'src\s*=\s*"([^"]+)"', value, re.I)
    if m:
        value = m.group(1)

    try:
        u = urlparse(value)
    except Exception:
        raise ValidationError("無法解析連結，請貼上『發布到網頁→嵌入』的連結。")

    host_ok = u.hostname and u.hostname.endswith("google.com")
    path_ok = ("/presentation/" in u.path and
               ("/embed" in u.path or "/pub" in u.path or "/pubembed" in u.path))

    if not (host_ok and path_ok):
        raise ValidationError("請使用 Google 簡報『發布到網頁→嵌入』的連結（含 /embed、/pub 或 /pubembed）。")

    # If you want to normalize the value server-side:
    field.data = value

class BibleSearchForm(FlaskForm):
    book_name = SelectField("經卷", choices=bible_book_choices, validators=[DataRequired()])
    chapter = IntegerField(
        "章",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="Chapter must be a positive number.")
        ]
    )
    start_verse = IntegerField(
        "開始經節",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="Verse number must be a positive number.")
        ]
    )
    end_verse = IntegerField(
        "結束經節",
        validators=[
            DataRequired(),
            NumberRange(min=1, message="Verse number must be a positive number.")
        ]
    )
    translations = SelectMultipleField(
        "Choose Bible Translations",
        choices=[("NIV", "NIV"), ("CUNP", "和合本"), ("KOUGO", "口語訳")],
        option_widget=CheckboxInput(),
        widget=ListWidget(prefix_label=False),
        validators=[AtLeastOneSelected]
    )

    def validate(self, extra_validators=None):
        # Run default validation first
        if not super().validate(extra_validators):
            return False

        # Cross-field check
        if self.start_verse.data and self.end_verse.data:
            if self.start_verse.data > self.end_verse.data:
                self.end_verse.errors.append("End verse must be greater than or equal to start verse.")
                return False
        return True
    submit = SubmitField("搜尋")

class SermonMetadataForm(FlaskForm):
    service_type = StringField("聚會類別")
    jp_sermon_topic = StringField("日文講道主題")
    cn_sermon_topic = StringField("中文講道主題")
    speaker_name = StringField("講道者姓名")
    interpreter_name = StringField("翻譯人員姓名")
    opening_hymn = StringField("聚會開始讚美詩")
    closing_hymn = StringField("聚會結束讚美詩")
    pianist_name = StringField("司琴人員姓名")
    submit = SubmitField("更新")

class AnnouncementForm(FlaskForm):
    google_slide_url = TextAreaField(
        "Google Slide的連結",
        validators=[DataRequired()],
        render_kw={
            "rows": 3,                    # height (in text rows)
            "cols": 120,                  # width fallback (CSS will override)
            "class": "url-textarea",      # hook for CSS
            "placeholder": "貼上『發佈到網路 → 嵌入』取得的連結或 <iframe> 片段…"
        }
    )
    submit = SubmitField("更新", render_kw={"class": "btn btn-primary"})