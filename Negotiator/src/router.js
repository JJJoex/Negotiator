import { createRouter ,createWebHistory } from "vue-router"
import Introduction from "./pages/Introduction.vue"
import Preparation from "./pages/Preparation.vue"
import Ensurement from "./pages/Ensurement.vue"
import Negotiation from "./pages/Negotiation.vue"
import Finish from "./pages/Finish.vue"

const routes = [
    {path: '/introduction', component: Introduction},
    {path: '/preparation', component: Preparation},
    {path: '/ensurement', component: Ensurement},
    {path: '/negotiation', component: Negotiation},
    {path: '/finish', component: Finish},
    {path: '/', redirect: '/introduction' }, 
]

const router = createRouter({
    history : createWebHistory(),
    routes,
})

export default router
