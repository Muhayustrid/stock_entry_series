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

        frappe.call({
            method: 'stock_entry_series.overrides.material_request.get_naming_series',
            args: { material_request_type: frm.doc.material_request_type },
            callback: function(r) {
                const series = r.message;
                if (!series) return;

                if (frm.fields_dict.naming_series) {
                    let options = (frm.fields_dict.naming_series.df.options || '').split('\n').filter(Boolean);
                    if (!options.includes(series)) {
                        options.push(series);
                        frm.set_df_property('naming_series', 'options', options.join('\n'));
                    }
                }

                frm.set_value('naming_series', series);
            }
        });
    }
});
