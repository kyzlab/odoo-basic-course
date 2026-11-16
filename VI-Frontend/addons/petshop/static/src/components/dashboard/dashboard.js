/** @odoo-module */

import { Component, useState, onWillStart } from "@odoo/owl";
import { registry } from "@web/core/registry";
import { useService } from "@web/core/utils/hooks";

export class PetshopDashboard extends Component {
    static template = "petshop.Dashboard";

    setup() {
        this.orm = useService("orm");

        // Initialize state with loading flag and empty stats
        this.state = useState({
            loading: true,
            totalPets: 0,
            alivePets: 0,
            sickPets: 0,
            speciesCount: 0,
            byGender: [],
        });

        // onWillStart: async, runs BEFORE first render.
        // Odoo waits for the Promise to resolve, so stats appear on first paint.
        onWillStart(async () => {
            const stats = await this.orm.call(
                'petshop.pet',          // model
                'get_dashboard_stats',  // Python method
                [],                     // positional args
            );
            Object.assign(this.state, {
                totalPets: stats.total_pets,
                alivePets: stats.alive_pets,
                sickPets: stats.sick_pets,
                speciesCount: stats.species_count,
                byGender: stats.by_gender,
                loading: false,
            });
        });
    }
}

// Register with tag "petshop.dashboard" — must match ir.actions.client tag in XML.
registry.category("actions").add("petshop.dashboard", PetshopDashboard);