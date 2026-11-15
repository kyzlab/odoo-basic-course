/** @odoo-module */

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class MyTableWidget extends Component {
    static template = "petshop.MyTable";

    setup() {
        this.orm = useService("orm");   // ORM service: call Python methods from JS

        // Extract current record fields from props
        const rec = this.props.record ? this.props.record.data : {};
        const rows = [];
        for (const [key, rawVal] of Object.entries(rec)) {
            // Many2one fields come as {id, display_name} objects — extract display_name
            let val = rawVal;
            if (val && typeof val === 'object' && 'display_name' in val) {
                val = val.display_name;
            }
            if (val === false || val === undefined || val === null) continue;
            rows.push({ key, value: String(val) });
        }

        this.state = useState({
            title: 'Pet Information',   // will be updated by server
            rows,
        });

        // onWillStart: async hook, runs BEFORE first render.
        // Odoo waits for the Promise to resolve before painting the component.
        // This ensures the title from the server appears on first render, not after.
        onWillStart(async () => {
            try {
                const title = await this.orm.call(
                    'petshop.pet',         // model name
                    'get_table_title',     // Python method name
                    [],                    // positional args
                    { value: 'course.minhng.info' }   // keyword args
                );
                this.state.title = title;
            } catch (err) {
                console.warn('MyTableWidget: server call failed', err);
                // keep default title on error
            }
        });
    }

    onClickTitle() {
        alert(`Widget title: "${this.state.title}"`);
    }
}

registry.category("view_widgets").add("mytable", { component: MyTableWidget });
