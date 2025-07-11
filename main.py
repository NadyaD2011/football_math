from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium import webdriver

import argparse
import pandas
import time


# Получаем доступ chromedriver
def create_driver():
    custom_options = Options()
    custom_options.add_argument("--start-maximized")
    path_driver = Service(r'chromedriver.exe')
    driver = webdriver.Chrome(service=path_driver, options=custom_options)

    return driver


# Получаем все матчи в формате objects
def get_matchs(driver, link, class_name):
    driver.get(link)
    time.sleep(10)

    matchs = driver.find_elements(By.CLASS_NAME, class_name)

    return matchs


# Получаем все данные по матчам в формате list
def get_results(matchs):
    match_results = []

    for match in matchs:
        result = match.text.splitlines()

        if len(result) == 5:
            if result[-1].isdigit():
                result[-1] = int(result[-1])
                result[-2] = int(result[-2])

            match_results.append(result)

    return match_results


# Создаём отфильтрованную DataFrame
def create_df(match_results):
    colunms_name = [
        'status',
        'team_1',
        'team_2',
        'goals_1',
        'goals_2'
    ]

    df = pandas.DataFrame(match_results, columns=colunms_name)
    df = df.loc[df['status'] == 'Завершен']
    df = df.loc[df['goals_2'] < 2]

    return df


def main():
    # Получаем дынные из запуска файла
    parser = argparse.ArgumentParser(
        description="В этой программе вы можете отслеживать результаты матчей."
    )
    parser.add_argument(
        "-file",
        "--filename",
        help="Введите путь до файла в формате: имя_файла.xlsx",
        type=str,
        default='results_match.xlsx'
    )
    args = parser.parse_args()

    driver = create_driver()

    link = "https://www.flashscorekz.com/"
    class_name = 'event__match'

    matchs = get_matchs(driver, link, class_name)

    match_results = get_results(matchs)

    df = create_df(match_results)

    # Сохранение таблице в формате Excel таблицы
    file_name = args.filename
    df.to_excel(file_name, index=False)


if __name__ == "__main__":
    main()
