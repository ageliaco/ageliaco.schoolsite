# -*- coding: utf-8 -*-

CONTENT = {
  'MAIN_SECTIONS': [
         ('presentation', u'Presentation', u'presentation-title', 'Folder'),  # About
         ('vie-ecole', u'''Vie de l'école''', u'vie-ecole-title', 'Folder'),
         ('espace-pedagogique', u'Espace pedagogique', u'espace-pedagogique-title', 'Folder'),
         ('espace-administratif', u'Espace administratif', u'espace-administratif-title', 'Folder'),
        # ('presentation', u'Presentation', u'presentation-title', 'Folder'),
  ],
  
  'ABOUT_CHILDREN': [
         ('ecole', u'''L'école''', u'ecole-title', 'Folder'),
         ('etudes', u'''Les études''', u'etudes-title', 'Folder'),
         ('personnes', u'''Les personnes''', u'personnes-title', 'Folder'),
         ('contact', u'''Contact et accès''', u'contact-title', 'Folder'),         
  ],
  
  'VIE_ECOLE_CHILDREN': [
         ('associations', u'''Associations''', u'associations-title', 'Folder'),
         ('groupes', u'''Groupes''', u'groupes-title', 'Folder'),
         ('cafeteria', u'''Caféteria''', u'cafeteria-title', 'Folder'),
         ('sante-social', u'''Santé - Social''', u'sante-social-title', 'Folder'),         
         ('arts', u'''Arts''', u'arts-title', 'Folder'),
         ('sport', u'''Sport''', u'sport-title', 'Folder'),
         ('voyages-sorties', u'''Voyages - Sorties''', u'voyages-sorties-title', 'Folder'),
  ],
  
  'PEDAGOGIQUE_CHILDREN': [
         ('cours', u'''Cours''', u'cours-title', 'Folder'),
         ('disciplines', u'''Disciplines''', u'disciplines-title', 'DisciplineContainer'),
         ('plan-etudes-programmes', u'''Plan d'études et programmes''', u'plan-etudes-programmes-title', 'Folder'),

         ('options', u'''options''', u'options-title', 'Folder'),
         ('cours-facultatifs', u'''Cours facultatifs''', u'cours-facultatifs-title', 'Folder'),
         ('soutien-pedagogique', u'''Soutien pédagogique''', u'soutien-pedagogique-title', 'Folder'),
         ('integration-eleves-avec-handicap', u'''integration-eleves-avec-handicap''', u'integration-eleves-avec-handicap-title', 'Folder'),

         ('echanges-sejours', u'''echanges-sejours''', u'echanges-sejours-title', 'Folder'),
         ('centre-documentation', u'''Centre de documentation''', u'centre-documentation-title', 'Folder'),
         ('materiel-services-a-disposition', u'''materiel-services-a-disposition''', u'materiel-services-a-disposition-title', 'Folder'),

  ],
  
  'ADMINISTRATIF_CHILDREN': [  # NON EXHAUSTIVE... COMPLETE LATER...
         ('memento-eleves', u'''memento-eleves''', u'memento-eleves-title', 'Folder'),
         ('memento-enseignants', u'''memento-enseignants''', u'memento-enseignants-title', 'Folder'),
         ('autres-calendriers', u'''autres-calendriers''', u'autres-calendriers-title', 'Folder'),
       # ...
         ('gestion-des-liberations', u'''Gestion des libérations''', u'gestion-des-liberations-title', 'Folder'),
         
  ],

  # --- 3rd level ---
  
  'DISCIPLINES_CHILDREN': [
         ('anglais', u'''Anglais''', u'anglais-title', 'Discipline'),
         ('allemand', u'''Allemand''', u'allemand-title', 'Discipline'),
         ('mathematiques', u'''Mathematiques''', u'mathematiques-title', 'Discipline'),

         
  ],

}



LOCAL_GROUPS = [('DirectionGroup', 'direction'),

                ('Doyen1Group', 'doyen1'),
                ('Doyen2Group', 'doyen2'),
                ('Doyen3Group', 'doyen3'),
                ('Doyen4Group', 'doyen4'),
                ('Doyen5Group', 'doyen5'),
                
                ('EcranGroup', 'ecran'),
                ('InfoGroup', 'info'),
                ('LiberationsGroup', 'liberations'),
                ('SecretariatGroup', 'secretariat'),
              ]
          
