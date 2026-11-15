/** @odoo-module */
// The /** @odoo-module */ directive is REQUIRED.
// Without it, Odoo will not recognize this file as an ES module
// and you will get "Cannot use import statement outside a module" error.

import { Component, useState } from "@odoo/owl";
import { registry } from "@web/core/registry";

function getTodayAsInteger() {
    const today = new Date();
    const yy    = String(today.getFullYear()).slice(-2);
    const mm    = String(today.getMonth() + 1).padStart(2, '0');
    const dd    = String(today.getDate()).padStart(2, '0');
    return parseInt(`${yy}${mm}${dd}`, 10);  // e.g. 260527 for 2026-05-27
}

export class Counter extends Component {
    static template = "petshop.Counter";   // must match t-name in XML

    setup() {
        // useState creates a reactive state proxy.
        // When state.value changes, the component automatically re-renders.
        this.state = useState({ value: getTodayAsInteger() });
    }

    increment() {
        this.state.value++;
    }

    decrement() {
        this.state.value--;
    }

    reset() {
        this.state.value = getTodayAsInteger();
    }
}

// Register the widget so it can be used in XML views with <widget name="counter"/>
registry.category("view_widgets").add("counter", { component: Counter });
