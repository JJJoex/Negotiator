import { createMemoryHistory, createRouter ,createWebHistory } from "vue-router"
import Introduction from "./pages/Introduction.vue"
import Negotiation from "./pages/Negotiation.vue"
import Finish from "./pages/Finish.vue"
import Preparation from "./pages/Preparation.vue"
import Ensurement from "./pages/Ensurement.vue"

const routes = [
    {path: '/description', component: Introduction},
    {path: '/preparation', component: Preparation},
    {path: '/ensurement', component: Ensurement},
    {path: '/negotiation', component: Negotiation},
    {path: '/finish', component: Finish},
    { path: '/', redirect: '/description' }, 
]

const router = createRouter({
    // history: createMemoryHistory(),
    history : createWebHistory(),
    routes,
})

export default router
