# import pygame
# import math

# class PlayerRenderer:
#     # def draw(self, screen, player):
#     #     screen.blit(player.animation.get_frame(), (player.x, player.y))

#     def draw(self, screen, player):
#         trail = player.trail

#         if len(trail) > 1:
#             # ===== 7 màu cầu vồng =====
#             rainbow_colors = [
#                 (255, 0, 0),     # đỏ
#                 (255, 127, 0),   # cam
#                 (255, 255, 0),   # vàng
#                 (0, 255, 0),     # xanh lá
#                 (0, 255, 255),   # cyan
#                 (0, 0, 255),     # xanh dương
#                 (139, 0, 255),   # tím
#             ]

#             # ===== vẽ từng segment =====
#             for i in range(1, len(trail)):
#                 x1, y1 = trail[i - 1]
#                 x2, y2 = trail[i]

#                 # vector hướng bay
#                 dx = x2 - x1
#                 dy = y2 - y1

#                 length = math.hypot(dx, dy)
#                 if length == 0:
#                     continue

#                 # vector vuông góc
#                 nx = -dy / length
#                 ny = dx / length

#                 # fade alpha
#                 t = i / len(trail)
#                 alpha = int(255 * t * 0.8)

#                 # ===== vẽ 7 line =====
#                 for j, color in enumerate(rainbow_colors):
#                     offset = (j - 3) * 3  # 7 line centered

#                     start_pos = (x1 + nx * offset, y1 + ny * offset)
#                     end_pos   = (x2 + nx * offset, y2 + ny * offset)

#                     # vẽ lên surface alpha
#                     line_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
#                     pygame.draw.line(
#                         line_surf,
#                         (*color, alpha),
#                         start_pos,
#                         end_pos,
#                         4
#                     )
#                     screen.blit(line_surf, (0, 0))

#         # ===== PLAYER =====
#         frame = player.animation.get_frame()
#         screen.blit(frame, (player.x, player.y))

# import pygame
# import math

# class PlayerRenderer:
#     def draw(self, screen, player):
#         trail = player.trail

#         if len(trail) > 2:
#             rainbow_colors = [
#                 (255, 0, 0),
#                 (255, 127, 0),
#                 (255, 255, 0),
#                 (0, 255, 0),
#                 (0, 255, 255),
#                 (0, 0, 255),
#                 (139, 0, 255),
#             ]

#             # ===== tạo curve mượt hơn bằng nội suy =====
#             smooth_trail = []
#             for i in range(len(trail) - 1):
#                 x1, y1 = trail[i]
#                 x2, y2 = trail[i + 1]

#                 # nội suy thêm điểm giữa
#                 for t in [0.0, 0.5]:
#                     x = x1 + (x2 - x1) * t
#                     y = y1 + (y2 - y1) * t
#                     smooth_trail.append((x, y))

#             smooth_trail.append(trail[-1])

#             # ===== vẽ trail =====
#             for i in range(1, len(smooth_trail)):
#                 x1, y1 = smooth_trail[i - 1]
#                 x2, y2 = smooth_trail[i]

#                 t = i / len(smooth_trail)

#                 # fade mượt hơn (power curve)
#                 alpha = int(255 * (t ** 2))

#                 # độ dày giảm dần
#                 width = int(6 * (t) + 1)

#                 for j, color in enumerate(rainbow_colors):
#                     offset_y = (j - 3) * 3

#                     start_pos = (x1, y1 + offset_y)
#                     end_pos   = (x2, y2 + offset_y)

#                     # surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

#                     pygame.draw.line(
#                         screen,
#                         (*color, alpha),
#                         start_pos,
#                         end_pos,
#                         width
#                     )

#                     # screen.blit(surf, (0, 0))

#         # ===== PLAYER =====
#         frame = player.animation.get_frame()
#         screen.blit(frame, (player.x, player.y))

# import pygame

# class PlayerRenderer:
#     def draw(self, screen, player):
#         trail = player.trail

#         rainbow_colors = [
#             (255, 0, 0),
#             (255, 127, 0),
#             (255, 255, 0),
#             (0, 255, 0),
#             (0, 255, 255),
#             (0, 0, 255),
#             (139, 0, 255),
#         ]

#         # ===== DRAW TRAIL =====
#         for i in range(len(trail)):
#             p = trail[i]
#             x, y = p["pos"]
#             life = p["life"]

#             alpha = int(255 * life)

#             # độ dày giảm theo life
#             width = int(8 * life + 1)

#             for j, color in enumerate(rainbow_colors):
#                 offset_y = (j - 3) * 2

#                 surf = pygame.Surface((20, 20), pygame.SRCALPHA)

#                 pygame.draw.circle(
#                     surf,
#                     (*color, alpha),
#                     (10, 10 + offset_y),
#                     width
#                 )

#                 screen.blit(surf, (x - 10, y - 10))

#         # ===== PLAYER =====
#         frame = player.animation.get_frame()
#         screen.blit(frame, (player.x, player.y))

# import pygame
# import math

# class PlayerRenderer:
#     def draw(self, screen, player):
#         trail = player.trail

#         if len(trail) < 2:
#             frame = player.animation.get_frame()
#             screen.blit(frame, (player.x, player.y))
#             return

#         rainbow_colors = [
#             (255, 0, 0),
#             (255, 127, 0),
#             (255, 255, 0),
#             (0, 255, 0),
#             (0, 255, 255),
#             (0, 0, 255),
#             (139, 0, 255),
#         ]

#         # ===== DRAW LINE TRAIL =====
#         for i in range(1, len(trail)):
#             p1 = trail[i - 1]
#             p2 = trail[i]

#             x1, y1 = p1["pos"]
#             x2, y2 = p2["pos"]

#             life = p2["life"]

#             # ===== FADE THEO ĐUÔI =====
#             alpha = int(255 * life)
#             width = int(8 * (life ** 1.5) + 1)

#             # ===== VECTOR HƯỚNG =====
#             dx = x2 - x1
#             dy = y2 - y1
#             length = math.hypot(dx, dy)

#             if length == 0:
#                 continue

#             # vector vuông góc
#             nx = -dy / length
#             ny = dx / length

#             # ===== VẼ 7 LINE =====
#             for j, color in enumerate(rainbow_colors):
#                 offset = (j - 3) * 2  # khoảng cách giữa các màu

#                 start_pos = (x1 + nx * offset, y1 + ny * offset)
#                 end_pos   = (x2 + nx * offset, y2 + ny * offset)

#                 pygame.draw.line(
#                     screen,
#                     (*color, alpha),
#                     start_pos,
#                     end_pos,
#                     width
#                 )

#         # ===== PLAYER =====
#         frame = player.animation.get_frame()
#         screen.blit(frame, (player.x, player.y))

import pygame
import math

class PlayerRenderer:
    def draw(self, screen, player):
        trail = player.trail

        if len(trail) < 2:
            frame = player.animation.get_frame()
            screen.blit(frame, (player.x, player.y))
            return
        
        rainbow_colors = [
            (255, 0, 0),
            (255, 127, 0),
            (255, 255, 0),
            (0, 255, 0),
            (0, 255, 255),
            (0, 0, 255),
            (139, 0, 255),
        ]

        # ===== LẤY DANH SÁCH POINT =====
        points = [p["pos"] for p in trail]

        # ===== LÀM MƯỢT (INTERPOLATION) =====
        smooth = []
        for i in range(len(points) - 1):
            x1, y1 = points[i]
            x2, y2 = points[i + 1]

            for t in [0.0, 0.3, 0.6]:
                x = x1 + (x2 - x1) * t
                y = y1 + (y2 - y1) * t
                smooth.append((x, y))

        smooth.append(points[-1])
        
        # ===== VẼ RIBBON =====
        for j, color in enumerate(rainbow_colors):
            offset_points = []

            for i in range(len(smooth)):
                x, y = smooth[i]

                # tính hướng để offset
                if i == 0:
                    dx, dy = smooth[i+1][0] - x, smooth[i+1][1] - y
                else:
                    dx, dy = x - smooth[i-1][0], y - smooth[i-1][1]

                length = math.hypot(dx, dy)
                if length == 0:
                    nx, ny = 0, 0
                else:
                    nx = -dy / length
                    ny = dx / length

                offset = (j - 3) * 3

                ox = x + nx * offset
                oy = y + ny * offset

                offset_points.append((ox, oy))

            # ===== FADE THEO ĐUÔI =====
            alpha_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

            for i in range(1, len(offset_points)):
                t = i / len(offset_points)

                alpha = int(255 * (t ** 2))   # mờ dần cực mượt
                width = int(8 * t + 1)

                pygame.draw.line(
                    alpha_surf,
                    (*color, alpha),
                    offset_points[i - 1],
                    offset_points[i],
                    width
                )

            screen.blit(alpha_surf, (0, 0))
        
        import random

        # ===== DRAW PARTICLES =====
        for p in player.particles:
            x, y = p["pos"]
            life = p["life"]
            size = p["size"]
            angle = p["angle"]
            color = p["color"]

            alpha = int(255 * (life ** 1.5))

            # ===== tạo surface nhỏ =====
            surf_size = size * 6
            surf = pygame.Surface((surf_size, surf_size), pygame.SRCALPHA)

            cx = surf_size // 2
            cy = surf_size // 2

            # ===== STAR SHAPE =====
            # vẽ dấu cộng (+)
            # pygame.draw.line(surf, (*color, alpha), (cx - size, cy), (cx + size, cy), 2)
            # pygame.draw.line(surf, (*color, alpha), (cx, cy - size), (cx, cy + size), 2)
            pygame.draw.line(surf, color, (cx - size, cy), (cx + size, cy), 2)
            pygame.draw.line(surf, color, (cx, cy - size), (cx, cy + size), 2)

            # vẽ dấu X
            # pygame.draw.line(surf, (*color, alpha), (cx - size, cy - size), (cx + size, cy + size), 1)
            # pygame.draw.line(surf, (*color, alpha), (cx - size, cy + size), (cx + size, cy - size), 1)
            pygame.draw.line(surf, color, (cx - size, cy - size), (cx + size, cy + size), 1)
            pygame.draw.line(surf, color, (cx - size, cy + size), (cx + size, cy - size), 1)

            # ===== glow mềm =====
            pygame.draw.circle(surf, (*color, int(alpha * 0.2)), (cx, cy), size * 2)

            surf.set_alpha(alpha)
            # ===== scale theo life (twinkle effect) =====
            scale = 0.5 + life * 0.8
            new_size = int(surf_size * scale)
            surf = pygame.transform.scale(surf, (new_size, new_size))

            # ===== rotate =====
            surf = pygame.transform.rotate(surf, angle)

            rect = surf.get_rect(center=(x, y))
            
            screen.blit(surf, rect)
        # for p in player.particles:
        #     x, y = p["pos"]
        #     life = p["life"]
        #     size = p["size"]

        #     alpha = int(255 * life)

        #     # màu random nhẹ (kim tuyến)
        #     color = random.choice([
        #         (255, 255, 255),   # trắng
        #         (255, 255, 100),   # vàng
        #         (100, 255, 255),   # xanh sáng
        #         (255, 150, 255),   # hồng
        #     ])

        #     surf = pygame.Surface((size*4, size*4), pygame.SRCALPHA)

        #     # ⭐ vẽ dạng sao đơn giản
        #     pygame.draw.circle(surf, (*color, alpha), (size*2, size*2), size)

        #     # thêm glow nhẹ
        #     pygame.draw.circle(surf, (*color, int(alpha*0.3)), (size*2, size*2), size*2)

        #     screen.blit(surf, (x - size*2, y - size*2))

        # rainbow_colors = [
        #     (255, 0, 0),
        #     (255, 127, 0),
        #     (255, 255, 0),
        #     (0, 255, 0),
        #     (0, 255, 255),
        #     (0, 0, 255),
        #     (139, 0, 255),
        # ]

        # # ===== LẤY DANH SÁCH POINT =====
        # points = [p["pos"] for p in trail]

        # # ===== LÀM MƯỢT (INTERPOLATION) =====
        # smooth = []
        # for i in range(len(points) - 1):
        #     x1, y1 = points[i]
        #     x2, y2 = points[i + 1]

        #     for t in [0.0, 0.3, 0.6]:
        #         x = x1 + (x2 - x1) * t
        #         y = y1 + (y2 - y1) * t
        #         smooth.append((x, y))

        # smooth.append(points[-1])

        # # ===== VẼ RIBBON =====
        # for j, color in enumerate(rainbow_colors):
        #     offset_points = []

        #     for i in range(len(smooth)):
        #         x, y = smooth[i]

        #         # tính hướng để offset
        #         if i == 0:
        #             dx, dy = smooth[i+1][0] - x, smooth[i+1][1] - y
        #         else:
        #             dx, dy = x - smooth[i-1][0], y - smooth[i-1][1]

        #         length = math.hypot(dx, dy)
        #         if length == 0:
        #             nx, ny = 0, 0
        #         else:
        #             nx = -dy / length
        #             ny = dx / length

        #         offset = (j - 3) * 3

        #         ox = x + nx * offset
        #         oy = y + ny * offset

        #         offset_points.append((ox, oy))

        #     # ===== FADE THEO ĐUÔI =====
        #     alpha_surf = pygame.Surface(screen.get_size(), pygame.SRCALPHA)

        #     for i in range(1, len(offset_points)):
        #         t = i / len(offset_points)

        #         alpha = int(255 * (t ** 2))   # mờ dần cực mượt
        #         width = int(8 * t + 1)

        #         pygame.draw.line(
        #             alpha_surf,
        #             (*color, alpha),
        #             offset_points[i - 1],
        #             offset_points[i],
        #             width
        #         )

        #     screen.blit(alpha_surf, (0, 0))

        # ===== PLAYER =====
        frame = player.animation.get_frame()
        screen.blit(frame, (player.x, player.y))