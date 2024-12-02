import { createMemoryHistory, createRouter } from "vue-router"
import Introduction from "./pages/Introduction.vue"
import Bidding from "./pages/Bidding.vue"
import Finish from "./pages/Finish.vue"
import Preparation from "./pages/Preparation.vue"

const routes = [
    {path: '/', component: Introduction},
    {path: '/preparation', component: Preparation},
    {path: '/bidding', component: Bidding},
    {path: '/finish', component: Finish},
]

const router = createRouter({
    history: createMemoryHistory(),
    routes,
})

export default router
