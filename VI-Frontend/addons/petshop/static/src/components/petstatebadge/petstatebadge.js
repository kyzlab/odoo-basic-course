/** @odoo-module */

import { Component } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { standardFieldProps } from "@web/views/fields/standard_field_props";

// Map each state value → Bootstrap badge color and display label.
// Add or remove entries to match your petshop.pet state selection values.
const STATE_CONFIG = {
    available:  { label: "Available",  color: "success" },
    reserved:   { label: "Reserved",   color: "warning" },
    sick:       { label: "Sick",       color: "danger"  },
    quarantine: { label: "Quarantine", color: "warning" },
    sold:       { label: "Sold",       color: "info"    },
    removed:    { label: "Removed",    color: "secondary" },
};

export class PetStateBadge extends Component {
    static template = "petshop.PetStateBadge";

    // Spread standardFieldProps into static props so OWL validates
    // incoming props correctly (record, name, readonly, required, etc.).
    static props = { ...standardFieldProps };

    /**
     * Compute badge config from the current field value.
     * props.name  — the technical field name (e.g., "state")
     * props.record.data — plain object with all field values of the open record
     */
    get badgeConfig() {
        const value = this.props.record.data[this.props.name];
        return STATE_CONFIG[value] || { label: value || "—", color: "secondary" };
    }
}

// Register in "fields" registry.
// supportedTypes: restrict usage to Selection fields only.
// Odoo warns in the browser console if this widget is applied to a wrong type.
registry.category("fields").add("pet_state_badge", {
    component: PetStateBadge,
    displayName: "Pet State Badge",
    supportedTypes: ["selection"],
});