def select_obj(self, evemt):
    x = evemt.x
    y = evemt.y
    for ant in self.ants_list:
        shift = ant.cell_size / 2
        if not ant.selected \
                and not ant.stuck \
                and abs(ant.x - x) <= shift and abs(ant.y - y) <= shift:
            print(ant.name, 'выбран')
            ant.selected = True
            # self.bind('<Button-1>', ant.move_obj)          # было/работает
            self.bind('<Button-1>', lambda event, arg=ant: self.move_obj(event, arg))
            self.itemconfig(ant.obj, image=ant.photo_selected_True)
            if not ant.loading:
                for berry in self.berries_list:
                    if berry.i == ant.i and berry.j == ant.j and not berry.taken:
                        btn_take = TakeButton(self, "Взять", ant.x, ant.y)
                        self.btn_list.append(btn_take)
                        break
                for ant_friend in self.ants_list:
                    if (ant_friend.i, ant_friend.j) in self.search_hex_nearby(ant.i, ant.j) and ant_friend.stuck:
                        print("Друг в беде!", ant_friend.name, ant_friend.i, ant_friend.j)
                        # self.bind('<Button-1>', self.ant_direction)

            elif ant.loading:
                if self.hexes_dict.get((ant.i, ant.j)).is_anthill:
                    btn_drop = DropButton(self, 'Положить', ant.x, ant.y)
                    self.btn_list.append(btn_drop)
                    print(ant.name, 'дома с ягодкой')
            break