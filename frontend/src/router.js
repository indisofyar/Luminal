import {createRouter, createWebHistory} from 'vue-router'
import Home from './pages/Home.vue'
import SignIn from './pages/SignIn.vue'
import SignUp from './pages/SignUp.vue'
import ResetPassword from './pages/ResetPassword.vue'
import Dashboard from './pages/Dashboard.vue'

const routerHistory = createWebHistory()

const router = createRouter({
    scrollBehavior(to) {
        if (to.hash) {
            window.scroll({top: 0})
        } else {
            document.querySelector('html').style.scrollBehavior = 'auto'
            window.scroll({top: 0})
            document.querySelector('html').style.scrollBehavior = ''
        }
    },
    history: routerHistory,
    routes: [
        {
            path: '/',
            component: Home
        },
        {
            path: '/signin',
            component: SignIn
        },
        {
            path: '/signup',
            component: SignUp
        },
        {
            path: '/reset-password',
            component: ResetPassword
        },
        {
            path: '/demo',
            component: Dashboard
        },
        {
            path: '/demo/',
            component: Dashboard
        }
    ]
})

export default router
