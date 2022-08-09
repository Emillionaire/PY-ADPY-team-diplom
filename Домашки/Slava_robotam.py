import re
from itertools import product
from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
with open("phonebook_raw.csv", encoding='utf-8') as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)
  list1 = []
  list2 = []
  list3 = []
  for contact in contacts_list[1:]:
    contact1 = ' '.join(contact)
    patt = r"([А-ЯЁ][а-яё]+)\s?([А-ЯЁ][а-яё]+)\s?([А-ЯЁ][а-яё]+)?"
    res = re.sub(patt, r"\1 \2 \3 ", contact1)
    list1.append(res)
  for i, name in enumerate(list1):
    for v, n in enumerate(list1[i+1:]):
      if ' '.join(name.split()[:2]) in n:
        for z in n.split():
          if z not in name:
            name = name + ' ' +z
            list1[i] = name
        list1.remove(n)
  for i, con in enumerate(list1):
    patt = r"([А-ЯЁ][а-яё]+\s[А-ЯЁа-яё]+\s[А-ЯЁа-яё]+\s+Минфин|ФНС)\s+(.+)(\+.*\d)"
    res = re.sub(patt, r"\1 \3 \2", con)
    if res:
      list1[i] = res
  for con in list1:
    patt = r"(\+7|8)\s?\(?(495)\)?\s?-?([0-9]{3})-?\s?([0-9]{2})\s?-?([0-9]{2})\s?\(?(доб.)?\s?([0-9]+)?\s?\s?\)?"
    res2 = re.sub(patt, r"+7(\2)\3-\4-\5 \6\7", con)
    list2.append(res2)
  for con in list2:
    list3.append(" ".join(con.split()))
  for i, con in enumerate(list3):
    patt = r"([А-ЯЁа-яё*\s[А-ЯЁа-яё]*\s[А-ЯЁа-яё]*)\s(ФНС|Минфин)\s?\s?(.*\d)?\s?\s?(.\d?\s)?"
    # res = re.findall(patt, con)
    res = re.sub(patt, r"\1,\2,\3,\4", con).split(',')
    if res[-1] == '':
      res.pop(-1)
    list3[i] = res
  list3.insert(0, contacts_list[0])

  with open("phonebook.csv", "w") as f:
    datawriter = csv.writer(f)
    # Вместо contacts_list подставьте свой список
    datawriter.writerows(list3)




