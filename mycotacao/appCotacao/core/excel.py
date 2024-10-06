from openpyxl import workbook
import datetime

def ExportarExcel(endereco_arquivo):
    wb = workbook.Workbook()
    # ws_cotacao = wb.create_sheet("Cotacao")
    ws_cotacao = wb['Sheet']
    ws_cotacao.title = "Cotacao"
    ws_cotacao['A4'] = "Bem Vindo ao OpenPyXL"
    ws_cotacao['A2'] = datetime.datetime.now()
    wb.save(endereco_arquivo)