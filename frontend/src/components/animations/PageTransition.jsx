import { motion } from "framer-motion";

const PageTransition = ({ children, direction = 1 }) => {
    return (
        <motion.div
            initial={{ x: 100 * direction, opacity: 0 }}
            animate={{ x: 0, opacity: 1 }}
            exit={{ x: -100 * direction, opacity: 0 }}
            transition={{
                type: "spring",
                stiffness: 400,
                damping: 20,
                mass: 0.1,
                duration: 0.1
            }}
            class="h-full w-full"
        >
            {children}
        </motion.div>
    );
};

export default PageTransition;