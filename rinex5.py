#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os
from datetime import datetime
import shutil
import zipfile
import logging
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


## Génération du fichier de logs
logging.basicConfig(filename='log.log',level=logging.DEBUG,\
                    format='%(asctime)s -- %(name)s -- %(levelname)s -- %(message)s')

# Déclarations
Source='/home/Rinex/source'
Dest='/home/sauvegardefichiers'
TransfertsRGP='/home/TransfertsRGP/'
Fichiermdp='/home/Rinex/mdp.txt'

d=datetime.now()
a=d.strftime('%Y')
année=a[-2:]

brut='.' + année + 'o'
hatanaka='.' + année + 'd'
navigation_gps='.' + année + 'n'
navigation_glonass='.' + année + 'g'


## Configuration du serveur de mail

port = 587
smtp_server = "smtp.gmail.com"
sender_email = "sandrine.morey71@gmail.com"             # Adresse expedition
receiver_email = "sandrine.morey@sat-info.fr"           # Adresse  reception

# Récupération du mot de passe

with open(Fichiermdp,'r') as fich:
    for i in range(2):
        pwd = fich.readline()

# Fonction d'envoi de mail

def envoi_mail(message):
	msg = MIMEMultipart()
	msg['From'] = sender_email
	msg['To'] = receiver_email
	msg['Subject'] = 'Alarme traitement Rinex'
	msg.attach(MIMEText(message))
	mailserver = smtplib.SMTP(smtp_server,port)
	mailserver.ehlo()
	mailserver.starttls()
	mailserver.ehlo()
	mailserver.login(sender_email, pwd)
	mailserver.sendmail(sender_email,receiver_email, msg.as_string())
	mailserver.quit()

## Récupération des fichiers bruts
liste=os.listdir(Source)

## Vérification de la présence de fichiers
if not liste:
	logging.info('Pas de fichiers bruts')
	envoi_mail('Pas de fichiers bruts disponibles')						# Envoi d'un mail d'alarme

## Déplacement vers le fichier contenant les fichiers bruts
os.chdir(Source)


## Compression des fichiers en Hatanaka
try:
	for f in liste:
		if f.endswith(brut):
			args=f
			comp="/home/Rinex/" + "RNX2CRX " + args + " -f"   			# l'option -f écrase les fichiers existants
			os.system(comp)                                	  			# compression des fichiers en Hatanaka
			shutil.copy2(args, Dest)                          			# copie des fichiers ".o" vers le répertoire de sauvegarde
			## shutil.copy2 permet de conserver les permissions et les dates des dernières modifications des fichiers
			os.remove(args)                                  			# suppression des fichiers ".o"
			logging.info('Compression Hatanaka des fichiers sources effectuée')	# Génération des log
except OSError as err:
	print(err)
	logging.error(err)
	envoi_mail('Une erreur est survenue lors du traitement des fichiers Rinex.\n Consulter le fichier de logs pour plus de détails')

## Création du fichier zip si le fichier Hatanaka existe
try:
	for f in os.listdir(Source):
		racine=f.rsplit('.', 1)[0]
		nom=racine+hatanaka
		if f.endswith(hatanaka):
			shutil.make_archive(nom, 'zip', Source, f)      			# Création de l'archive zip contenant les fichiers Hatanaka
			logging.info('Création des archives Zip du fichier hatanaka ' + f + ' réussi') # Génération des log
			os.remove(f)                                                 		# suppression des fichiers Hatanaka non compressé
			logging.info('Suppression des fichiers Hatanaka non zippés: ' + f)	#Génération des log
except OSError as err:
	print(err)
	logging.error(err)
	envoi_mail('Une erreur est survenue lors du traitement des fichiers Rinex.\n Consulter le fichier de logs pour plus de détails')

## Ajout des fichiers de navigation à l'archive
try:
	for f in os.listdir(Source):
		if f.endswith(navigation_gps) or f.endswith(navigation_glonass):
			navigation=f
			archives=navigation[0:8] + '.' + année + 'd.zip'
			zfile=zipfile.ZipFile(archives, 'a')
			zfile.write(navigation, compress_type=zipfile.ZIP_DEFLATED)
			zfile.close()
			os.remove(f)								# suppresion des fichiers de navigation ajoutés à l'archive
			logging.info('Ajout des fichiers de navigation à l archive ' + f + ' réussi') # Génération des log 
except OSError as err:
	print(err)
	logging.error(err)
	envoi_mail('Une erreur est survenue lors du traitement des fichiers Rinex.\n Consulter le fichier de logs pour plus de détails')

## Déplacement des fichiers zip pour transfert vers le RGP
zip = os.listdir(Source)
try:
	for f in zip:
		if f.endswith(".zip"):
			shutil.move(f,TransfertsRGP)
			logging.info('Transfert des fichiers compresser pour envoie au RGP ' + f + ' réussi') # Génération des log 
except OSError as err:
	print(err)
	logging.error(err)
	envoi_mail('Une erreur est survenue lors du traitement des fichiers Rinex.\n Consulter le fichier de logs pour plus de détails')
