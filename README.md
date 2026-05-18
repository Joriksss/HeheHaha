<?xml version="1.0" encoding="UTF-8"?>

<project>
    <title>Краткая инструкция по работе с базой данных</title>

    <description>
        Это краткая инструкция по работе с базой данных для проекта на Streamlit.
        Здесь описаны основные моменты, которые нужно учитывать при создании,
        заполнении и проверке базы данных.
    </description>

    <database>
        <name>base</name>

        <manual_fill>
            <item>
                Базу данных можно заполнить вручную через DBeaver.
            </item>
            <item>
                Для удобной вставки SQL-кода можно использовать сочетания клавиш:
                сначала Ctrl+C для копирования, затем Ctrl+Shift+V для вставки в базу данных.
            </item>
            <item>
                В DBeaver можно выделять нужные части SQL-кода отдельно:
                создание таблиц, SELECT-запросы, INSERT-запросы и другие команды.
            </item>
        </manual_fill>

        <important_rules>
            <rule>
                Порядок полей в базе данных, SQL-запросах и Python-коде должен быть одинаковым.
            </rule>
            <rule>
                Если в таблице указан один порядок полей, то при INSERT-запросе
                данные в Python должны передаваться в такой же последовательности.
            </rule>
            <rule>
                Если порядок перепутать, данные могут вставляться неправильно,
                либо приложение будет выдавать ошибку.
            </rule>
        </important_rules>

        <table_creation_order>
            <description>
                Таблицы нужно создавать в правильном порядке, потому что между ними
                есть связи через внешние ключи.
            </description>

            <first_step>
                <description>
                    Сначала создаются маленькие справочные таблицы.
                </description>

                <tables>
                    <table>roles</table>
                    <table>units</table>
                    <table>manufacturers</table>
                    <table>suppliers</table>
                    <table>categories</table>
                    <table>pickup_points</table>
                </tables>
            </first_step>

            <second_step>
                <description>
                    После этого создаются основные таблицы, которые используют связи
                    со справочными таблицами.
                </description>

                <tables>
                    <table>users</table>
                    <table>products</table>
                    <table>orders</table>
                    <table>order_items</table>
                </tables>
            </second_step>
        </table_creation_order>

        <foreign_keys>
            <description>
                В базе данных используются внешние ключи. Например, товар связан
                с категорией, производителем, поставщиком и единицей измерения.
                Поэтому сначала должны существовать справочные таблицы, а потом
                уже таблица товаров.
            </description>
        </foreign_keys>

        <checking>
            <item>
                После создания базы нужно проверить, что таблицы реально появились.
            </item>
            <item>
                Также нужно проверить, что приложение подключается именно к нужному файлу базы.
            </item>
            <item>
                Если приложение пишет, что таблицы нет, значит Python может брать базу
                из другой папки.
            </item>
        </checking>

        <images>
            <description>
                Изображения товаров можно заменить на свои.
                По умолчанию можно использовать файл picture.png.
            </description>
        </images>

        <final_note>
            В целом нужно проверить путь к базе, порядок создания таблиц,
            порядок полей в INSERT-запросах и наличие данных. После этого
            приложение должно работать корректно.
        </final_note>
    </database>
</project>
