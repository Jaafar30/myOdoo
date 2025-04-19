# -*- coding: utf-8 -*-
# from odoo import http


# class JaffarModule(http.Controller):
#     @http.route('/jaffar_module/jaffar_module', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/jaffar_module/jaffar_module/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('jaffar_module.listing', {
#             'root': '/jaffar_module/jaffar_module',
#             'objects': http.request.env['jaffar_module.jaffar_module'].search([]),
#         })

#     @http.route('/jaffar_module/jaffar_module/objects/<model("jaffar_module.jaffar_module"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('jaffar_module.object', {
#             'object': obj
#         })

