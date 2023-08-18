from datacenter.models import Schoolkid, Mark, Chastisement
from datacenter.models import Commendation, Lesson, Subject


def get_schoolkid(name_schoolkid: str) -> Schoolkid:
    try:
        schoolkid = Schoolkid.objects.get(full_name__contains=name_schoolkid)
        return schoolkid
    except Schoolkid.DoesNotExist:
        print('Не найдено ниодного ученика с таким именем')
    except Schoolkid.MultipleObjectsReturned:
        print('Найдено несколько учеников с таким именем')


def fix_marks(name_schoolkid: str, points=4):
    schoolkid = get_schoolkid(name_schoolkid)
    if not schoolkid:
        return

    marks_count = Mark.objects.filter(
        schoolkid=schoolkid, points__lte=3).update(points=points)

    print(f'Изменено {marks_count} оценок')


def remove_chastisements(name_schoolkid: str):
    schoolkid = get_schoolkid(name_schoolkid)
    if not schoolkid:
        return

    chastisement = Chastisement.objects.filter(schoolkid=schoolkid)
    chastisement_count = chastisement.count()
    chastisement.delete()
    print(f'Удалено {chastisement_count} замечаний')


def get_last_lesson(name_lesson: str, schoolkid: Schoolkid) -> Lesson:
    try:
        subjects = Subject.objects.get(
            title__contains=name_lesson,
            year_of_study=schoolkid.year_of_study
        )
    except Subject.DoesNotExist:
        print('У даннного ученика нет такого предмета')
        return
    except Subject.MultipleObjectsReturned:
        print('Найдено несколько предметов с таким наименованием')
        return

    lessons = Lesson.objects.filter(
        year_of_study=schoolkid.year_of_study,
        group_letter=schoolkid.group_letter,
        subject=subjects.first()
    ).order_by('-date')

    return lessons.first()


def create_commendation(name_schoolkid: str, name_lesson: str,
                        commendation_text='Хвалю!'):
    schoolkid = get_schoolkid(name_schoolkid)
    lesson = get_last_lesson(name_lesson, schoolkid)
    if not schoolkid or not lesson:
        return

    Commendation.objects.create(
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher,
        text=commendation_text,
        created=lesson.date
    )
    print('Рекомендация создана')
