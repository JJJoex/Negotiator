import { createRouter ,createWebHistory } from "vue-router"
import Introduction from "./pages/Introduction.vue"
import Preparation from "./pages/Preparation.vue"
import PreparationSetting from "./pages/Preparation/Setting.vue"
import PreparationMyInterest from "./pages/Preparation/MyInterest.vue"
import PreparationMyIssue from "./pages/Preparation/MyIssue.vue"
import PreparationOpponentInterest from "./pages/Preparation/OpponentInterest.vue"
import PreparationOpponentIssue from "./pages/Preparation/OpponentIssue.vue"
import PreparationConfirmation from "./pages/Preparation/Confirmation.vue"
import Negotiation from "./pages/Negotiation.vue"
import Finish from "./pages/Finish.vue"

const routes = [
    {path: '/description', component: Introduction},
    {path: '/preparation', component: Preparation, 
        children: [
            {path: 'setting', component: PreparationSetting},
            {path: 'myInterest', component: PreparationMyInterest},
            {path: 'myIssue', component: PreparationMyIssue},
            {path: 'opponentInterest', component: PreparationOpponentInterest},
            {path: 'opponentIssue', component: PreparationOpponentIssue},
            {path: 'confirmation', component: PreparationConfirmation},
        ]
    },
    {path: '/negotiation', component: Negotiation},
    {path: '/finish', component: Finish},
    {path: '/', redirect: '/description' }, 
]

const router = createRouter({
    // history: createMemoryHistory(),
    history : createWebHistory(),
    routes,
})

export default router
