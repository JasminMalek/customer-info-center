const Welcome = () => import('./components/MainPage.vue')
const CustomerList = () => import('./components/customer/List.vue')
const CustomerCreate = () => import('./components/customer/Add.vue')
const CustomerEdit = () => import('./components/customer/Edit.vue')
const CustomerShow = () => import('./components/customer/Show.vue')

export const routes = [
    {
        name: 'home',
        path: '/',
        component: Welcome
    },
    {
        name: 'customerList',
        path: '/customer',
        component: CustomerList
    },
    {
        name: 'customerEdit',
        path: '/customer/:id/edit',
        component: CustomerEdit
    },{
        name: 'customerShow',
        path: '/customer/:id',
        component: CustomerShow
    },
    {
        name: 'customerAdd',
        path: '/customer/add',
        component: CustomerCreate
    }
]
