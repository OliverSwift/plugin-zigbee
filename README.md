# plugin ZIGBEE Jeedom

Ceci est une copie (légale) du plugin zigbee de Jeedom.
En effet, la licence pour ces fichiers est GPL et AGPL et spécifie bien les attributs copyleft de la GPL.

Cette version contient des modifications concernant le support de quelques objets (notamment Tuya) et qui ne sont pas
encore supporté par Jeedom. C'est souvent une question de version de zha-quirks. Ce dernier est soit pas encore au niveau dans
Jeedom, soit tout simplement les récents commits ne sont pas publiés dans les repo officiels.

L'installation de ce plugin est triviale, il suffit de copier ces sources dans /var/www/html/plugins de Jeedom

Autres points, il y a de très nombreux points de failles de sécurité qui seront adressés ultérieurement. Et pas spécifiques au plugin mais bien à Jeedom lui même. A suivre.

# Nouveaux dispositifs supportés

|Photo |Zigbee id | Référence/Modèle|
|------|----------|-----------------|
|![TZE200_myd45weu.TS0601](https://raw.githubusercontent.com/OliverSwift/plugin-zigbee/master/core/config/devices/tuya/TZE200_myd45weu.TS0601.png)|TZE200_myd45weu.TS0601|QT-07S - Soil Humidity Sensor|
|![TZE200_locansqn.TS0601](https://raw.githubusercontent.com/OliverSwift/plugin-zigbee/master/core/config/devices/tuya/TZE200_locansqn.TS0601.png)|TZE200_locansqn.TS0601|Capteur Température et Humidité avec Affichage de la date|
|![TZE204_t1blo2bj.TS0601](https://raw.githubusercontent.com/OliverSwift/plugin-zigbee/master/core/config/devices/tuya/TZE204_t1blo2bj.TS0601.png)|TZE204_t1blo2bj.TS0601|Sirène Neo (sans capteurs)|
|![TZE200_6rdj8dzm.TS0601](https://raw.githubusercontent.com/OliverSwift/plugin-zigbee/master/core/config/devices/tuya/TZE200_6rdj8dzm.TS0601.png)|TZE200_6rdj8dzm.TS0601|Tête thermostatique Avatto TRV06|

