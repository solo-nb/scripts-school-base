from datacenter.models import Schoolkid, Mark, Chastisement
from datacenter.models import Commendation, Lesson, Subject


def get_schoolkid(name_schoolkid: str) -> Schoolkid:
    schoolkids = Schoolkid.objects.filter(full_name__contains=name_schoolkid)
    schoolkids_count = schoolkids.count()
    if schoolkids_count == 0:
        print('Не найдено ниодного ученика с таким именем')
        return
    if schoolkids_count > 1:
        print('Найдено несколько учеников с таким именем')
        return

    return schoolkids.first()


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
    subjects = Subject.objects.filter(
        title__contains=name_lesson,
        year_of_study=schoolkid.year_of_study
    )
    subjects_count = subjects.count()
    if subjects_count == 0:
        print('У даннного ученика нет такого предмета')
        return
    if subjects_count > 1:
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

    commendation = Commendation.objects.create(
        schoolkid=schoolkid,
        subject=lesson.subject,
        teacher=lesson.teacher,
        text=commendation_text,
        created=lesson.date
    )
    commendation.save()
    print('Рекомендация создана')
