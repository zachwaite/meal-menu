Meal Menu Management
======================

This repository contains apps related to meal planning and management for
commercial businesses.

* meal_menu_core - core models, methods and utilites
* meal_menu_views - backend views
* meal_menu_reports - report boilerplate
* meal_menu_api - external interfaces


The core set of models is designed to provide everything needed to create a
meal plan using meal cycles of varying length, which can generate individual
meals for your dining locations and meal times. What is left for the project
implementation is to create Many2one fields representing the slots for each
meal as these are the things that will dictate your interface. You can filter
the items using domain.

e.g. 

ENTREE = self.env.ref('my_module.meal_item_category_entree')
APPETIZER = self.env.ref('my_module.meal_item_category_entree')

entree_1 = fields.Many2one('meal.item', domain=[('category_id', '=', ENTREE.id)])
appetizer_1 = fields.Many2one('meal.item', domain=[('category_id', '=', APPETIZER.id)])


