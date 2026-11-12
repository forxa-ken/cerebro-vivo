# -*- coding: utf-8 -*-
"""Spec 046 fase 1: diagramas Mermaid (flowchart y sequenceDiagram) dibujados como SVG dentro de las diapositivas."""
import importlib.util
import os
import re
import shutil
import sys
import tempfile
import unittest
import xml.etree.ElementTree as ET

RAIZ = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
GUARDIANES = os.path.join(RAIZ, ".brain", "guardianes")
sys.path.insert(0, GUARDIANES)
import diagramas  # noqa: E402


def cargar_diapositivas():
    e = importlib.util.spec_from_file_location("diapositivas_dg", os.path.join(GUARDIANES, "diapositivas.py"))
    m = importlib.util.module_from_spec(e)
    e.loader.exec_module(m)
    return m


dp = cargar_diapositivas()
FLUJO = "flowchart LR\n  A[Idea] --> B[Spec]\n  B -->|programar| C{¿Pruebas?}\n  C -->|sí| D([Hecha])\n  C -.->|no| B\n"
SECUENCIA = "sequenceDiagram\n  autonumber\n  participant D as Darwin\n  D->>Claude: pide\n  Claude-->>D: responde\n  Note over D,Claude: cierre\n  Claude->>Claude: revisa\n"


def textos_svg(svg):
    return [e.text for e in ET.fromstring(svg).iter() if e.tag.endswith("tspan")]


class Flujo(unittest.TestCase):
    def test_dibuja_un_nodo_por_caja_y_una_flecha_por_arista(self):
        svg = diagramas.pintar(FLUJO)
        raiz = ET.fromstring(svg)  # el SVG es XML válido
        self.assertEqual(sum(1 for e in raiz.iter() if e.tag.endswith(("rect", "polygon", "ellipse"))), 4)
        self.assertEqual(len(re.findall(r'marker-end="url\(#dg-f\d+\)"', svg)), 4)
        for t in ("Idea", "Spec", "¿Pruebas?", "Hecha", "programar", "sí", "no"):
            self.assertIn(t, textos_svg(svg))

    def test_cada_dibujo_tiene_su_propio_id_de_marcador(self):
        ids = [re.search(r'<marker id="([^"]+)"', diagramas.pintar("flowchart LR\n A --> B")).group(1) for _ in range(2)]
        self.assertNotEqual(ids[0], ids[1])

    def test_las_cuatro_direcciones_y_graph_valen(self):
        for d in ("LR", "RL", "TB", "TD", "BT"):
            ET.fromstring(diagramas.pintar("flowchart %s\n A --> B --> C" % d))
        ET.fromstring(diagramas.pintar("graph TD\n A --> B"))

    def test_lr_pone_las_capas_a_la_derecha_y_td_hacia_abajo(self):
        def centros(cab):
            svg = diagramas.pintar(cab + "\n A[uno] --> B[dos]")
            return [float(x) for x in re.findall(r'<rect class="dg-c" x="([\d.]+)"', svg)], [float(y) for y in re.findall(r'<rect class="dg-c" x="[\d.]+" y="([\d.]+)"', svg)]
        xs, ys = centros("flowchart LR")
        self.assertGreater(xs[1], xs[0])
        xs, ys = centros("flowchart TD")
        self.assertGreater(ys[1], ys[0])

    def test_un_ciclo_y_una_flecha_a_si_mismo_no_cuelgan_el_dibujo(self):
        ET.fromstring(diagramas.pintar("flowchart LR\n A --> B\n B --> A\n A --> A"))

    def test_cadena_en_una_sola_linea_y_etiqueta_con_guiones(self):
        svg = diagramas.pintar("flowchart LR\n A --> B -- texto largo --> C")
        self.assertEqual(len(re.findall(r'marker-end="url\(#dg-f\d+\)"', svg)), 2)
        self.assertIn("texto largo", textos_svg(svg))

    def test_el_texto_se_escapa(self):
        svg = diagramas.pintar('flowchart LR\n A["<script>alert(1)</script>"] --> B')
        self.assertNotIn("<script", svg)
        self.assertIn("&lt;script&gt;", svg)
        ET.fromstring(svg)


class Secuencia(unittest.TestCase):
    def test_participantes_mensajes_y_notas(self):
        svg = diagramas.pintar(SECUENCIA)
        ET.fromstring(svg)
        textos = textos_svg(svg)
        for t in ("Darwin", "Claude", "1. pide", "2. responde", "3. revisa", "cierre"):
            self.assertIn(t, textos)
        self.assertEqual(len(re.findall(r'marker-end="url\(#dg-f\d+\)"', svg)), 3)

    def test_el_mensaje_a_si_mismo_cabe_en_el_ancho(self):
        svg = diagramas.pintar("sequenceDiagram\n A->>A: un texto bastante largo")
        ancho = float(re.search(r'viewBox="0 0 ([\d.]+)', svg).group(1))
        x = float(re.search(r'<tspan x="([\d.]+)"[^>]*>un texto', svg).group(1))
        self.assertGreater(ancho, x + len("un texto bastante largo") * 7)


class Errores(unittest.TestCase):
    def pide(self, codigo, esperado):
        with self.assertRaises(ValueError) as c:
            diagramas.pintar(codigo)
        self.assertEqual(str(c.exception), esperado)

    def test_tipos_y_bloques_no_soportados(self):
        self.pide("pie\n  a: 1", "tipo")
        self.pide("classDiagram\n  A <|-- B", "tipo")
        self.pide("flowchart LR\n subgraph S\n A --> B\n end", "tipo")
        self.pide("sequenceDiagram\n loop cada día\n A->>B: x\n end", "tipo")

    def test_sintaxis_rota(self):
        self.pide("flowchart LR\n A -->", "sintaxis")
        self.pide("flowchart XX\n A --> B", "sintaxis")
        self.pide("sequenceDiagram\n esto no es un mensaje", "sintaxis")
        self.pide("", "sintaxis")

    def test_limites(self):
        self.pide("flowchart LR\n" + "\n".join("N%d --> N%d" % (i, i + 1) for i in range(16)), "limite")
        self.pide("sequenceDiagram\n" + "\n".join("P%d->>P%d: x" % (i, i + 1) for i in range(7)), "limite")


class EnLasDiapositivas(unittest.TestCase):
    def setUp(self):
        self.d = tempfile.mkdtemp()
        self.addCleanup(shutil.rmtree, self.d, True)

    def convertir(self, texto):
        md = os.path.join(self.d, "p.md")
        with open(md, "w", encoding="utf-8", newline="") as f:
            f.write(texto)
        rutas, n, _, _ = dp.convertir(md, abrir=False)
        with open(rutas[0], encoding="utf-8") as f:
            return f.read()

    def test_un_bloque_mermaid_sale_como_svg_y_el_html_no_pide_nada_a_internet(self):
        pagina = self.convertir("# A\n\n---\n\n```mermaid\n%s```\n" % FLUJO)
        self.assertIn('<svg class="dg"', pagina)
        self.assertNotIn("<pre><code>flowchart", pagina)
        self.assertIn(".dg-c{", pagina)
        self.assertIsNone(re.search(r"(src|href)=\"https?://", pagina))
        self.assertIn("default-src 'none'", pagina)

    def test_un_bloque_que_no_se_puede_dibujar_cae_a_texto_y_avisa(self):
        pagina = self.convertir("# A\n\n---\n\n```mermaid\npie\n a: 1\n```\n")
        self.assertIn("<pre><code>pie", pagina)
        self.assertEqual(dp.AVISOS, ["tipo"])

    def test_los_bloques_de_codigo_normales_siguen_igual(self):
        pagina = self.convertir("# A\n\n```python\nprint(1)\n```\n")
        self.assertIn("<pre><code>print(1)", pagina)
        self.assertEqual(dp.AVISOS, [])

    def test_las_separaciones_dentro_de_un_bloque_mermaid_no_parten_la_diapositiva(self):
        pagina = self.convertir("# A\n\n```mermaid\nflowchart LR\n A --> B\n```\n")
        self.assertEqual(pagina.count('<section class="d">'), 1)

    def test_el_aviso_sale_en_el_idioma_del_proyecto(self):
        from textos import TEXTOS
        for lang in ("es", "en"):
            for k in ("diap_diagrama_texto", "diap_diagrama_tipo", "diap_diagrama_sintaxis", "diap_diagrama_limite"):
                self.assertIn(k, TEXTOS[lang])


if __name__ == "__main__":
    unittest.main()
