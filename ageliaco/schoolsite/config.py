# -*- coding: utf-8 -*-

CONTENT = {
  'MAIN_SECTIONS': [
         ('presentation', u'Présentation', u'presentation-title', 'Folder'),  # About
         ('vie-ecole', u'''Vie de l'école''', u'vie-ecole-title', 'Folder'),
         ('espace-pedagogique', u'Espace pedagogique', u'espace-pedagogique-title', 'Folder'),
         ('espace-administratif', u'Espace administratif', u'espace-administratif-title', 'Folder'),

  ],
  
  'ABOUT_CHILDREN': [
         ('ecole', u'''L'école''', u'ecole-title', 'Folder'),
         ('etudes', u'''Les études''', u'etudes-title', 'Folder'),
         ('personnes', u'''Les personnes''', u'personnes-title', 'Folder'),
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

         ('disciplines', u'''Disciplines''', u'disciplines-title', 'Folder'),

         ('plan-etudes-programmes', u'''Plan d'études et programmes''', u'plan-etudes-programmes-title', 'Folder'),

         ('options', u'''options''', u'options-title', 'Folder'),
         ('cours-facultatifs', u'''Cours facultatifs''', u'cours-facultatifs-title', 'Folder'),
         ('soutien-pedagogique', u'''Soutien pédagogique''', u'soutien-pedagogique-title', 'Folder'),
         ('integration-eleves-avec-handicap', u'''integration-eleves-avec-handicap''', u'integration-eleves-avec-handicap-title', 'Folder'),

         ('echanges-sejours', u'''echanges-sejours''', u'echanges-sejours-title', 'Folder'),
         ('centre-documentation', u'''Centre de documentation''', u'centre-documentation-title', 'Folder'),
         ('materiel-services-a-disposition', u'''materiel-services-a-disposition''', u'materiel-services-a-disposition-title', 'Folder'),

  ],
  
  'ADMINISTRATIF_CHILDREN': [ 
         ('memento-eleves', u'''memento-eleves''', u'memento-eleves-title', 'Folder'),
         ('memento-enseignants', u'''memento-enseignants''', u'memento-enseignants-title', 'Folder'),
         ('autres-calendriers', u'''autres-calendriers''', u'autres-calendriers-title', 'Folder'),

         ('inscriptions-transferts', u'''inscriptions-transferts''', u'inscriptions-transferts-title', 'Folder'),
         ('formulaires', u'''formulaires''', u'formulaires-title', 'Folder'),
         ('listes-horaires-coordonnees', u'''listes-horaires-coordonnees''', u'listes-horaires-coordonnees-title', 'Folder'),
         ('conference-presidents-de-groupe', u'''conference-presidents-de-groupe''', u'conference-presidents-de-groupe-title', 'Folder'),
         ('reglements', u'''reglements''', u'reglements-title', 'Folder'),
         
         ('infos-officielles--directives', u'''infos-officielles--directives''', u'infos-officielles--directives-title', 'Folder'),
         ('outils-informatiques-administratifs-pour-enseignants', u'''outils-informatiques-administratifs-pour-enseignants''', u'outils-informatiques-administratifs-pour-enseignants-title', 'Folder'),
         ('bureaux-de-gestion--bureaux-horaires', u'''espace-bureaux-de-gestion--bureaux-horaires''', u'espace-bureaux-de-gestion--bureaux-horaires-title', 'Folder'),

         ('gestion-des-liberations', u'''Gestion des libérations''', u'gestion-des-liberations-title', 'Folder'),
         
  ],

  # --- 3rd level ---
  ## Let's disable the 3rd level for now!
#   'PRESENTATION_ECOLE_CHILDREN': [
#          ('adresse', u'''Adresse''', u'adresse-title', 'Document', u'''Remplacez par votre texte...'''),
#          ('contact', u'''Contact''', u'contact-title', 'Document', u'''Remplacez par votre texte...'''),
#          ('acces', u'''Accès''', u'acces-title', 'Document', u'''Remplacez par votre texte...'''),
#          ('horaires', u'''Horaires''', u'horaires-title', 'Document', u'''Remplacez par votre texte...'''),
#          ('utilisation-locaux', u'''Utilisation des locaux''', u'utilisation-locaux-title', 'Document', u'''Remplacez par votre texte...'''),
#          ('circulation-et-parking', u'''Circulation et parking''', u'circulation-et-parking-title', 'Document', u'''Remplacez par votre texte...'''),
#          ('securite', u'''Sécurité''', u'securite-title', 'Document', u'''Remplacez par votre texte...'''),
# 
#   ],
# 
#   'PRESENTATION_ETUDES_CHILDREN': [
#          ('etudes-dans-notre-ecole', u'''Les études dans notre école''', u'etudes-dans-notre-ecole-title', 'Document', u'''Remplacez par votre texte...'''),
#          # TODO : Cabler les 2 liens...
#   ],
#   
#   'PRESENTATION_PERSONNES_CHILDREN': [
#          ('direction', u'''Direction''', u'direction-title', 'Document', u'''Remplacez par votre texte...'''),
#          ('conseil-de-direction', u'''Conseil de direction''', u'conseil-de-direction-title', 'Document', u'''Remplacez par votre texte...'''),
#          ('enseignants', u'''Enseignants''', u'enseignants-title', 'Document', u'''Remplacez par votre texte...'''),
#          ('personnel-administratif-et-technique', u'''Personnel administratif et technique''', u'personnel-administratif-et-technique-title', 'Document', u'''Remplacez par votre texte...'''),
#          ('eleves', u'''Elèves''', u'eleves-title', 'Document', u'''Remplacez par votre texte...'''),
# 
#   ],
  
}


# Technical sections to be used for Administering the website (excluded from NAV)
SITEADMIN_CONTENT = {
  'MAIN_SECTIONS': [
         ('delegation-des-taches', u'delegation-des-taches', u'delegation-des-taches-title', 'Folder'),
         ('contenus-a-modifier-chaque-annee', u'''Contenus à modifier chaque année''', u'contenus-a-modifier-chaque-annee-title', 'Folder'),
         ('gestion-des-evenements', u'Gestion des événements', u'gestion-des-evenements-title', 'Folder'),
         ('aide-et-documentation', u'Aide et documentation', u'aide-et-documentation-title', 'Folder'),
         ('homepage', u'ACCUEIL', u'homepage-title', 'Folder'),
  ],

  'HOMEPAGE_CHILDREN': [
         ('footer', u'''Footer''', u'footer-title', 'Folder'),
         ('vitrines', u'''Vitrines''', u'vitrines-title', 'Folder'),
         ('best-of', u'''Best of''', u'best-of-title', 'Folder'),
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
          
