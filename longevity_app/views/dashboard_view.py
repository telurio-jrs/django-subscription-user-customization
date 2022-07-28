import math
import os

from db.library.utils.helper import paginator
from db.models import Article, ArticlesWeight
from django.db.models import Q
from django.shortcuts import redirect, render
from django.views import View
from numpy.random import choice

PG_LIMIT = int(os.getenv('PG_LIMIT', 12))


class DashboardView(View):
    def get(self, *args, **kwargs):
        pg = int(self.request.GET.get('pg', 1))
        number_of_itens = pg * PG_LIMIT

        articles_all = ArticlesWeight.objects.values(
            'article_id',
            'wei_probability'
        )

        if self.request.GET.get('search'):
            articles = Article.objects.filter(
                Q(
                    Q(art_title__icontains=self.request.GET.get('search', '')) |  # noqa: E501
                    Q(art_abstract__icontains=self.request.GET.get('search', '')) |  # noqa: E501
                    Q(art_authors__icontains=self.request.GET.get('search', ''))  # noqa: E501
                )
            ).values(
                'id',
                'art_title',
                'art_abstract',
                'art_authors',
                'art_publish_year'
            )

            # Counting total pages
            total_pages = math.ceil(articles.count()/PG_LIMIT)

            # Separate rows for exposure
            pg_offset = (pg * PG_LIMIT) - PG_LIMIT
            articles = articles[pg_offset:(pg_offset+PG_LIMIT)]
        else:
            ids = list(i['article_id'] for i in articles_all)
            probs = list(float(i['wei_probability']) for i in articles_all)
            prob_sum = sum(probs)
            probs[-1] += 1 - prob_sum
            # answers = itertools.ifilter(lambda x: x.id not in ids, answers)

            draw = list(choice(ids, number_of_itens, p=probs))

            # Select rows
            articles = Article.objects.filter(
                id__in=draw[-PG_LIMIT:]
            ).values(
                'id',
                'art_title',
                'art_abstract',
                'art_authors',
                'art_publish_year'
            )

            # Counting total pages
            articles_all = Article.objects.all().count()
            total_pages = math.ceil(articles_all/PG_LIMIT)

        # Set page range
        pg_range = paginator(pg, total_pages)

        context = {
            'articles': articles,
            'filter': {
                'search': self.request.GET.get('search', '')
            },
            'pages': {
                'pg': pg,
                'total_pg': total_pages,
                'pg_range': pg_range
            }
        }

        # set messages, if applicable
        if 'success' in self.request.session:
            context['success'] = self.request.session.get('success')
            del self.request.session['success']
        elif 'error' in self.request.session:
            context['error'] = self.request.session.get('error')
            del self.request.session['error']

        return render(
            request=self.request,
            template_name='longevity_app/pages/dashboard.html',
            context=context
        )

    def post(self, *args, **kwargs):
        # get existing entry from database
        data = Article.objects.filter(
            id=self.request.POST['del_article']
        ).first()

        # updating data and saving - for delete status = 0
        if data.art_score > 2:
            data.art_score -= 2
            data.save()

        self.request.session['success'] = 'Article removed successfully.'
        return redirect('longevity_app:dashboard')
