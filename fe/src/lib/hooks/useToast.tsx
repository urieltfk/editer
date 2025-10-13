import toast from 'react-hot-toast'

export const useToast = () => {
  return {
    success: (message: string, duration?: number) => {
      toast.success(message, { duration })
    },
    error: (message: string, duration?: number) => {
      toast.error(message, { duration: duration || 5000 })
    },
    info: (message: string, duration?: number) => {
      toast(message, { duration, icon: 'ℹ️' })
    },
    warning: (message: string, duration?: number) => {
      toast(message, { duration, icon: '⚠️' })
    },
    loading: (message: string) => {
      return toast.loading(message)
    },
    dismiss: (toastId?: string) => {
      toast.dismiss(toastId)
    },
  }
}

