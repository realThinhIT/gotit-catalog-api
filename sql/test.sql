-- 1234567

INSERT INTO `user` (`id`,`created`,`updated`,`username`,`email`,`name`,`password_hash`) VALUES (1,'2019-06-16 11:56:30','2019-06-16 11:56:30','thinhnd','thinhnd.ict@gmail.com','Thinh Nguyen','$2b$10$Wt6HGBqAEs8P3EQ3WOw44eGTqz2HybYFiq5fDkMCm2dNRYjcIwqne');
INSERT INTO `user` (`id`,`created`,`updated`,`username`,`email`,`name`,`password_hash`) VALUES (2,'2019-06-16 16:04:58','2019-06-16 16:04:58','thinhnd2','thinhnd.ict2@gmail.com','Thinh Nguyen','$2b$10$pRyaFxsdJKMBEuiAaTNeqePOKDLoP0jCS.AyDXzZOl85KnAr/.Z36');

INSERT INTO `category` (`id`, `created`, `updated`, `name`, `description`) VALUES (1, '2019-06-16 15:23:42', '2019-06-16 15:23:42', 'Mobile Phones', 'Phones from international manufacturers and brands.');
INSERT INTO `category` (`id`, `created`, `updated`, `name`, `description`) VALUES (2, '2019-06-16 15:23:42', '2019-06-16 15:23:42', 'Laptops', 'Best laptops that can enhance your work performance.');
INSERT INTO `category` (`id`, `created`, `updated`, `name`, `description`) VALUES (3, '2019-06-16 15:23:42', '2019-06-16 15:23:42', 'Tablets', 'Go wherever you want, do whatever you want with these super flexible tablets.');
INSERT INTO `category` (`id`, `created`, `updated`, `name`, `description`) VALUES (4, '2019-06-16 15:23:42', '2019-06-16 15:23:42', 'Accessories', 'Make your devices prettier!');

INSERT INTO `item` (`id`, `created`, `updated`, `name`, `description`, `user_id`, `category_id`) VALUES (1, '2019-06-16 15:23:42', '2019-06-16 15:23:42', 'Apple iPhone XS Max', '', 1, 1);
INSERT INTO `item` (`id`, `created`, `updated`, `name`, `description`, `user_id`, `category_id`) VALUES (2, '2019-06-16 15:23:42', '2019-06-16 15:23:42', 'Samsung Galaxy A50', '', 2, 1);
INSERT INTO `item` (`id`, `created`, `updated`, `name`, `description`, `user_id`, `category_id`) VALUES (3, '2019-06-16 15:23:42', '2019-06-16 15:23:42', 'OPPO F11 6GB - 64GB', '', 2, 1);
INSERT INTO `item` (`id`, `created`, `updated`, `name`, `description`, `user_id`, `category_id`) VALUES (4, '2019-06-16 15:23:42', '2019-06-16 15:23:42', 'HP Envy 13-AH0027TU/Core i7-8550U', '', 1, 2);
INSERT INTO `item` (`id`, `created`, `updated`, `name`, `description`, `user_id`, `category_id`) VALUES (5, '2019-06-16 15:23:42', '2019-06-16 15:23:42', 'Samsung Galaxy Tab A 7" 2016', '', 1, 3);
INSERT INTO `item` (`id`, `created`, `updated`, `name`, `description`, `user_id`, `category_id`) VALUES (6, '2019-06-16 15:23:42', '2019-06-16 15:23:42', 'Huawei MediaPad T3 7.0 Prestige', '', 1, 3);
INSERT INTO `item` (`id`, `created`, `updated`, `name`, `description`, `user_id`, `category_id`) VALUES (7, '2019-06-16 15:23:42', '2019-06-16 15:23:42', 'Samsung Galaxy Tab E', '', 2, 3);
INSERT INTO `item` (`id`, `created`, `updated`, `name`, `description`, `user_id`, `category_id`) VALUES (8, '2019-06-16 15:23:42', '2019-06-16 15:23:42', 'Wireless Mouse Logitech M238', '', 2, 4);
INSERT INTO `item` (`id`, `created`, `updated`, `name`, `description`, `user_id`, `category_id`) VALUES (9, '2019-06-16 15:23:42', '2019-06-16 15:23:42', 'Wired Gaming Mouse Prolink G9501', '', 1, 4);