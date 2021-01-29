odoo.define('itis_temporary_fiscal_position.Sidebar', function (require) {
"use strict";

	var Sidebar = require('web.Sidebar');

	Sidebar.include({
	    _addToolbarActions: function (toolbarActions) {
	        var self = this;
	        this._super(toolbarActions)
	        if (_.contains(['sale.order', 'account.move', 'purchase.order'], self.env.model)){
	           var printItems = [{
	           		classname: 'o_sidebar_print',
					label: 'Upload to DMS', 
					url: 'https://itis-odoo.de/page/it-is-odoo-alfresco-version-12'
				}]
	           self._addItems('print', printItems);
	       	}  
	    },
	});

});