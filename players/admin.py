"""
admin for players
"""
from .models import  Player
from django.contrib import admin

#admin.site.register(Player)

@admin.register(Player)
class PlayerAdmin(admin.ModelAdmin):

    def formatted_market_value(self,obj):
        return f"{obj.market_value:,}" if obj.market_value is not None else "N/A"

    formatted_market_value.short_description = "Market value"


    list_display = ( 'id','name','age','caps','formatted_market_value','league_name','league_level')

    search_fields = ['id','name']
    list_filter = ['league_name']
    fieldsets = (
    (
        'Personal info',{
        'fields': ('name','date_of_birth','place_of_birth','citizenship','age','place_of_birth_flag')
    }
    ),
    (
        'Professional info',{
        'fields': ('club','national_team','caps','international_goals','market_value','main_position')
    }
    ),

    (
        'Additional info',{
        'fields': ('agency_info','club_stats','national_team_stats','current_season_stats')
    }
    )

    )


