frappe.ui.form.on('Material Request', {
    refresh: function(frm) {
        if (frm.is_new() && frm.doc.material_request_type) {
            const field_default = (frm.fields_dict.naming_series && frm.fields_dict.naming_series.df.default) || '';
            const fallback = "MAT-MR-.YYYY.-";
            if (!frm.doc.naming_series || frm.doc.naming_series === field_default || frm.doc.naming_series === fallback) {
                frm.trigger('material_request_type');
            }
        }
    },

    material_request_type: function(frm) {
        if (!frm.is_new() || !frm.doc.material_request_type) return;

        frappe.db.get_value('Naming Series Map',
            { document_type: 'Material Request', type_value: frm.doc.material_request_type },
            'naming_series'
        ).then(function(r) {
            const fallback = "MAT-MR-.YYYY.-";
            const series = (r && r.message && r.message.naming_series) ? r.message.naming_series : fallback;

            if (frm.fields_dict.naming_series) {
                let options = (frm.fields_dict.naming_series.df.options || '').split('\n').filter(Boolean);
                if (!options.includes(series)) {
                    options.push(series);
                    frm.set_df_property('naming_series', 'options', options.join('\n'));
                }
            }

            frm.set_value('naming_series', series);
        });
    }
});
