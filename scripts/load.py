from datetime import datetime
from pathlib import Path

import pandas as pd
from db.models import Article, ArticlesWeight


def run():
    now = datetime.now()
    data = pd.read_excel(f'{Path(__file__).resolve().parent}/article_data.xlsx')  # noqa: E501

    df = pd.DataFrame(data)
    df = df.reset_index()
    for index, row in df.iterrows():
        if row['title'] != 'NO_TITLE':
            title = row['title']
            abstract = row['abstract'] if row['abstract'] and row['abstract'] != 'NO_ABSTRACT' else None  # noqa: E501
            affiliations = row['affiliations'] if row['affiliations'] != 'NO_AFFILIATIONS' else None  # noqa: E501
            authors = row['authors'] if row['authors'] != 'NO_AUTHOR' else None  # noqa: E501
            journal = row['journal'] if row['journal'] != 'NO_JOURNAL' else None  # noqa: E501
            keywords = row['keywords'] if row['keywords'] != 'NO_KEYWORDS' else None  # noqa: E501
            url = row['url']
            date = row['date'] if row['date'] != 'NO_DATE' else None

            article_id = Article.objects.create(
                art_title=title,
                art_abstract=abstract,
                art_affiliations=affiliations,
                art_authors=authors,
                art_journal=journal,
                art_keyword=keywords,
                art_url=url,
                art_publish_year=date,
                art_date_created=now,
                art_date_updated=now
            )

            ArticlesWeight.objects.create(
                article=article_id,
                wei_score=10,
                wei_probability=0.001101321,
                wei_date_created=now,
                wei_date_updated=now
            )
