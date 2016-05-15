#!/usr/bin/env python
import os
import jinja2
import webapp2

from models import Film


template_dir = os.path.join(os.path.dirname(__file__), "templates")
jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(template_dir), autoescape=False)


class BaseHandler(webapp2.RequestHandler):

    def write(self, *a, **kw):
        return self.response.out.write(*a, **kw)

    def render_str(self, template, **params):
        t = jinja_env.get_template(template)
        return t.render(params)

    def render(self, template, **kw):
        return self.write(self.render_str(template, **kw))

    def render_template(self, view_filename, params=None):
        if not params:
            params = {}
        template = jinja_env.get_template(view_filename)
        return self.response.out.write(template.render(params))

class MainHandler(BaseHandler):
    def get(self):
        return self.render_template("chat.html")

class PosljiSporociloHandler(BaseHandler):
    def popravi_input(self, input):
        input = input.replace("<script>", "")
        input = input.replace("</script>", "")
        return input

    def post(self):
        film = self.request.get("ime")
        ocena = int(self.request.get("ocena"))
        slika = self.request.get("slika")

        film = self.popravi_input(film)
        ocena = int(self.popravi_input(ocena))
        slika = self.popravi_input(slika)

        if ocena > 5:
            self.render_template("napaka.html")
        else:
            sporocilo = Film(ime=film, ocena=ocena, slika=slika)
            sporocilo.put()
            return self.render_template("sporocilo-poslano.html")

class PrikaziSporocilaHandler(BaseHandler):
    def get(self):
        vsi_filmi = Film.query().order(Film.nastanek).fetch()

        view_vars = {
            "vsi_filmi": vsi_filmi
        }

        return self.render_template("prikazi_sporocila.html", view_vars)

class PosameznoSporociloHandler(BaseHandler):
    def get(self, film_id):
        film = Film.get_by_id(int(film_id))

        view_vars = {
            "film": film
        }

        return self.render_template("posamezno_sporocilo.html", view_vars)

class UrediSporociloHandler(BaseHandler):
    def get(self, film_id):
        film = Film.get_by_id(int(film_id))

        view_vars = {
            "film": film
        }

        return self.render_template("uredi_sporocilo.html", view_vars)

    def post(self, film_id):
        film = Film.get_by_id(int(film_id))
        film.ime = self.request.get("ime")
        film.ocena = int(self.request.get("ocena"))
        film.slika = self.request.get("slika")


        film.put()

        self.redirect("/film/" + film_id)

class IzbrisiSporociloHandler(BaseHandler):
    def get(self, film_id):
        film = Film.get_by_id(int(film_id))

        view_vars = {
            "film": film
        }

        return self.render_template("izbrisi_sporocilo.html", view_vars)

    def post(self, film_id):
        film = Film.get_by_id(int(film_id))
        film.key.delete()

        self.redirect("/prikazi-filme")


app = webapp2.WSGIApplication([
    webapp2.Route('/', MainHandler),
    webapp2.Route('/poslji-sporocilo', PosljiSporociloHandler),
    webapp2.Route('/prikazi-filme', PrikaziSporocilaHandler),
    webapp2.Route('/film/<film_id:\d+>', PosameznoSporociloHandler),
    webapp2.Route('/film/<film_id:\d+>/uredi', UrediSporociloHandler),
    webapp2.Route('/film/<film_id:\d+>/izbrisi', IzbrisiSporociloHandler),
], debug=True)
