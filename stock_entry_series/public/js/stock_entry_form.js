frappe.ui.form.on('Stock Entry', {
    refresh: function(frm) {
        if (frm.is_new() && frm.doc.stock_entry_type) {
            const field_default = (frm.fields_dict.naming_series && frm.fields_dict.naming_series.df.default) || '';
            const fallback = "MAT-STE-.YYYY.-";
            if (!frm.doc.naming_series || frm.doc.naming_series === field_default || frm.doc.naming_series === fallback) {
                frm.trigger('stock_entry_type');
            }
        }
    },

    stock_entry_type: function(frm) {
        if (!frm.is_new() || !frm.doc.stock_entry_type) return;

        frappe.db.get_value('Stock Entry Type', frm.doc.stock_entry_type, 'custom_naming_series')
            .then(function(r) {
                const fallback = "MAT-STE-.YYYY.-";
                const series = (r && r.message && r.message.custom_naming_series) ? r.message.custom_naming_series : fallback;

                if (frm.fields_dict.naming_series) {
                    let options = (frm.fields_dict.naming_series.df.options || '').split('\n').filter(Boolean);
                    if (series && !options.includes(series)) {
                        options.push(series);
                        frm.set_df_property('naming_series', 'options', options.join('\n'));
                    }
                }

                frm.set_value('naming_series', series);
            });
    }
});
