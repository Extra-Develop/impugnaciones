# import requests

from django.core.management.base import BaseCommand
from django.db import connection
from tmp.models import escrutinio1


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.create_cne_files()
        self.update_jrvs()

    def create_cne_files(self):
        with open('scripts/basicos/2uploadpresarauz.csv', 'w') as destiny_arauz, open('scripts/basicos/2uploadpreslasso.csv', 'w') as destiny_lasso:
            destiny_arauz.write("uid,cod_junta,sufragantes,nulos,blancos,arauz_votes\n")
            destiny_lasso.write("uid,lasso_votes\n")
            with open('scripts/basicos/CNE/PRESIDENTA_E_Y_VICEPRESIDENTA_E_2davuelta_test.csv', mode='r', encoding='cp1252') as source:
                # lines = requests.get("https://impugnaciones.andresarauz.ec/resultados/resultados_1.csv").text.split("\n")
                lines = source.readlines()
                for line in lines:
                    columna = line.split('|')
                    try:
                        uidcod = "{:02d}".format(int(columna[1])) + "{:03d}".format(int(columna[2])) + \
                                 "{:04d}".format(int(columna[4])) + "{:02d}".format(int(columna[5])) + \
                                 "{:03d}".format(int(columna[6])) + columna[7]
                        if columna[10] == '1030':
                            newline = uidcod + "," + columna[8] + "," + columna[11] + "," + columna[12] + "," + columna[13] + "," + \
                                      columna[14]
                            destiny_arauz.write(newline)
                        else:
                            newline = uidcod + "," + columna[14]
                            destiny_lasso.write(newline)
                    except Exception as e:
                        print(f'Error: \n{e}')

    def update_jrvs(self):
        # copiar CSV a BASE DE DATOS TEMPORAL
        cursor = connection.cursor()
        cursor.execute("TRUNCATE tmp_escrutinio1")
        insert_count = escrutinio1.objects.from_csv('scripts/basicos/2uploadpresarauz.csv', delimiter=",")
        print(f'{insert_count} registros cargados en la BD temporal')
        # Cargar datos de bd temporal a columna correspondiente
        cursor.execute(
            "UPDATE estructura_jrv v SET cne_arauz = e.arauz_votes, acta_cne = e.cod_junta, cnesufragantes=e.sufragantes, cnenulos=e.nulos, cneblancos=e.blancos FROM tmp_escrutinio1 e WHERE v.cod = e.uid")
        cursor.execute("TRUNCATE tmp_escrutinio1")
        insert_count = escrutinio1.objects.from_csv('scripts/basicos/2uploadpreslasso.csv', delimiter=",")
        print(f'{insert_count} registros cargados en la BD temporal')
        cursor.execute(
            "UPDATE estructura_jrv v SET cne_lasso = e.lasso_votes FROM tmp_escrutinio1 e WHERE v.cod = e.uid")

        # cursor.execute(
        #     "update comparacion_votacion set diff1 = cne1 - delegados  where delegados is not null and cne1 - delegados <> 0 ")
        # cursor.execute(
        #     "update comparacion_votacion set diff2 = cne1 - app_digitacion  where app_digitacion is not null and cne1 - app_digitacion <> 0 ")
        # destiny_arauz = open('basicos/diferencias.csv', 'w')
        # uidJRVDigpartidos = votacion.objects.raw(
        #     'select * from comparacion_votacion where diff1 is not null or diff2 is not null')

        # for uid in uidJRVDigpartidos:
        #     if uid.zona is None:
        #         zona = "0"
        #     else:
        #         zona = str(uid.zona.codzona)
        #
        #     line = str(uid.provincia.codprovincia) + "," + str(uid.canton.codcanton) + "," + str(
        #         uid.parroquia.codparroquia) + "," + zona + "," + \
        #            str(uid.recinto.codrecinto) + "," + str(uid.jrv.numero) + "," + uid.jrv.genero + "," + str(
        #         uid.dignidad.coddignidad) + "," + str(uid.partido.codpartido) + "," + str(uid.cne1) + "," + str(
        #         uid.diff1) + "," + str(uid.diff2) + "\n"
        #     destiny_arauz.write(line)
        print("diferencias generadas")
