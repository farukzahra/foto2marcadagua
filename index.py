import os
from PIL import Image, ImageDraw, ImageFont
import exifread

def converter_gps(gps, ref):
    graus = gps[0].num / gps[0].den
    minutos = gps[1].num / gps[1].den
    segundos = gps[2].num / gps[2].den
    coordenada = graus + (minutos / 60.0) + (segundos / 3600.0)
    if ref in ['S', 'W']:
        coordenada = -coordenada
    return coordenada

def obter_localizacao(imagem):
    with open(imagem, 'rb') as f:
        tags = exifread.process_file(f, details=False)

        try:
            lat = tags['GPS GPSLatitude']
            lat_ref = tags['GPS GPSLatitudeRef'].values
            lon = tags['GPS GPSLongitude']
            lon_ref = tags['GPS GPSLongitudeRef'].values
            latitude = converter_gps(lat.values, lat_ref)
            longitude = converter_gps(lon.values, lon_ref)
            return f"Lat: {latitude:.5f}, Lon: {longitude:.5f}"
        except KeyError:
            return None

def adicionar_marcadagua(caminho_imagem, texto, pasta_saida):
    with Image.open(caminho_imagem) as img:
        # Corrigir orientação EXIF, se necessário
        try:
            exif = img.getexif()
            if exif is not None:
                orientation_key = 274  # cf. ExifTags
                if orientation_key in exif:
                    orientation = exif[orientation_key]
                    if orientation == 3:
                        img = img.rotate(180, expand=True)
                    elif orientation == 6:
                        img = img.rotate(270, expand=True)
                    elif orientation == 8:
                        img = img.rotate(90, expand=True)
        except Exception:
            pass
        draw = ImageDraw.Draw(img)
        largura, altura = img.size
        try:
            fonte = ImageFont.truetype("arial.ttf", 48)  # Fonte maior
        except:
            fonte = ImageFont.load_default()
        margem = 10
        # Medir o tamanho do texto
        bbox = draw.textbbox((0, 0), texto, font=fonte)
        texto_largura = bbox[2] - bbox[0]
        texto_altura = bbox[3] - bbox[1]
        # Coordenadas do retângulo de fundo
        x = margem
        y = altura - texto_altura - margem
        # Desenhar fundo preto com um pouco de transparência
        fundo = Image.new('RGBA', (int(texto_largura + 20), int(texto_altura + 10)), (0, 0, 0, 180))
        img_rgba = img.convert('RGBA')
        img_rgba.paste(fundo, (int(x - 10), int(y - 5)), fundo)
        draw = ImageDraw.Draw(img_rgba)
        # Desenhar o texto por cima do fundo
        draw.text((x, y), texto, fill="white", font=fonte)
        nome = os.path.basename(caminho_imagem)
        caminho_saida = os.path.join(pasta_saida, nome)
        # Salvar mantendo o formato original
        img_final = img_rgba.convert(img.mode) if img.mode != 'RGBA' else img_rgba
        img_final.save(caminho_saida)

def processar_pasta(pasta_origem, pasta_saida):
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)

    for arquivo in os.listdir(pasta_origem):
        if arquivo.lower().endswith(('.jpg', '.jpeg', '.png')):
            caminho = os.path.join(pasta_origem, arquivo)
            localizacao = obter_localizacao(caminho)
            if localizacao:
                adicionar_marcadagua(caminho, localizacao, pasta_saida)
                print(f"✅ Processado: {arquivo}")
            else:
                print(f"⚠️  Sem localização: {arquivo}")

# Exemplo de uso
pasta_fotos = 'fotos_originais'
pasta_saida = 'fotos_com_marcadagua'

processar_pasta(pasta_fotos, pasta_saida)
