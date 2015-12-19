# -*- coding: utf-8 -*-
###############################################################################
#
#    Copyright (C) 2001-2014 Micronaet SRL (<http://www.micronaet.it>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as published
#    by the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
###############################################################################
import os
import sys
import logging
import openerp
import openerp.netsvc as netsvc
import openerp.addons.decimal_precision as dp
from openerp.osv import fields, osv, expression, orm
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from openerp import SUPERUSER_ID #, api
from openerp import tools
from openerp.tools.translate import _
from openerp.tools.float_utils import float_round as round
from openerp.tools import (DEFAULT_SERVER_DATE_FORMAT, 
    DEFAULT_SERVER_DATETIME_FORMAT, 
    DATETIME_FORMATS_MAP, 
    float_compare)


_logger = logging.getLogger(__name__)


class product_product_duty(osv.osv):
    ''' Extra fields for ETL in product.product
    ''' 
    _name = 'product.product.duty'
    _description = 'Product for duty'
    
    _columns = {
        'name': fields.char('Duty code', required=True, 
            help="Coded used for duty import / export"),
        'note': fields.text('Duty specific'),
        'type': fields.selection([
            ('code', 'Code'),
            ('protocol', 'Protocol'),
            ], 'Type of value', 
            help='Used for keep only one table and save 2 type of value'),
        }
    _defaults = {
        'type': lambda *x: 'code',
        }    
    
class product_product_adr(osv.osv):
    ''' Extra fields for ETL in product.product
    ''' 
    _inherit = 'product.product'
    
    _columns = {
        'duty_mineral_oil': fields.boolean('Mineral oil'),
        'duty_id': fields.many2one('product.product.duty', 'Duty', 
            domain=[('type', '=', 'code')]),
        'protocol_id': fields.many2one('product.product.duty', 'Protocol',
            domain=[('type', '=', 'protocol')]),
        'duty_type_reg': fields.selection([
            ('M', 'Material'),
            ('F', 'Product'),
            ], 'Duty reg. type'),
        'duty_type_store': fields.selection([
            ('C', 'C'),
            ], 'Type of store'),
        'duty_oil_perc': fields.float(
            'Oil %', digits=(16, 4)),
        }

class res_partner(osv.osv):
    ''' Add duty fields
    ''' 
    _inherit = 'res.partner'
    
    _columns = {
        'has_duty': fields.boolean('Has duty'),
        'duty_code': fields.char('Duty code', size=25), # 13
        
        # Company fields:
        
        }
class res_company_duty(osv.osv):
    ''' Add duty fields
    ''' 
    _name = 'res.company.duty'
    
    _columns = {
        'company_id': fields.many2one('res.company', 'Duty'), 
        
        # TODO required all?
        'duty_year': fields.char('Year', size=4, required=True),
        'duty_code': fields.char('Duty code', size=13),
        'duty_user_code': fields.char('Duty user code', size=4),
        'duty_flow_name': fields.char('Duty user code', size=12, 
            help='User code + Date MM + "." + interchange type (1) + '
                'Progr. interchange (2)'),
        'duty_id_company': fields.char('Company ID', size=3),
        'duty_office_name': fields.char('Office name', size=50),
        'duty_office_code': fields.char('Office code', size=20),
        'duty_protocol_number': fields.char('Prot. #', size=20),
        'duty_excise': fields.char('Excise', size=20),                
        
        }

class res_company(osv.osv):
    ''' Add duty fields
    ''' 
    _inherit = 'res.company'
    
    _columns = {
        'duty_ids': fields.one2many(
            'res.company.duty', 'company_id', 'Duty'), 
        }
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
