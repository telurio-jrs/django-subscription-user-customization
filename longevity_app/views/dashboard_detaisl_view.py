from db.models import Article
from django.shortcuts import render
from django.views import View


class DashboardDetailView(View):
    def get(self, *args, **kwargs):
        data = Article.objects.filter(
            id=kwargs['article']
        ).values(
            'art_title',
            'art_abstract',
            'art_affiliations',
            'art_authors',
            'art_journal',
            'art_keyword',
            'art_url',
            'art_publish_year'
        ).first()

        context = {
            'article': data
        }

        return render(
            request=self.request,
            template_name='longevity_app/pages/dashboard_details.html',
            context=context
        )
