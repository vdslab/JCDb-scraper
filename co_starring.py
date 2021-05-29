import json
import csv


def main():
    co_starring_count = {}
    with open('./jcdb/jcdb-movies.jsonlines', mode='r') as f_r:
        for line in f_r.readlines():
            obj = json.loads(line)
            if obj['カテゴリー'] == '成人映画' or obj['レーティング'] == 'R18+':
                continue

            if len(obj['出演者']) != 0:
                obj['出演者'] = list(
                    filter(lambda x: x['名前'] != None, obj['出演者']))
                obj['出演者'].sort(key=lambda x: x['名前'])

            for i, c_f in enumerate(obj['出演者']):
                name_f = c_f['名前']
                if name_f not in co_starring_count:
                    co_starring_count[name_f] = {}

                for c_t in obj['出演者'][i+1:]:
                    name_t = c_t['名前']
                    if name_t not in co_starring_count[name_f]:
                        co_starring_count[name_f][name_t] = 1
                    else:
                        co_starring_count[name_f][name_t] += 1

    with open('co_starring_count.csv', encoding='utf_8_sig', mode='w') as f_w:
        writer = csv.writer(f_w)
        data = []
        header = ['名前', '名前', '共演回数']
        for name_f in co_starring_count.keys():
            for name_t in co_starring_count[name_f].keys():
                data.append(
                    [name_f, name_t, co_starring_count[name_f][name_t]])
        data.sort(key=lambda x: x[2], reverse=True)
        data = list(filter(lambda x: x[2] > 1, data))
        data.insert(0, header)
        writer.writerows(data)

    with open('network_info.csv', encoding='utf_8_sig', mode='w') as f_w:
        writer = csv.writer(f_w)
        write_data = [['平均次数', 'エッジの個数']]
        edge_count = 0
        data = []
        average_degree = 0
        degree = {}
        for name_f in co_starring_count.keys():
            for name_t in co_starring_count[name_f].keys():
                data.append(
                    [name_f, name_t, co_starring_count[name_f][name_t]])
        edge_count = len(data)

        co_starring_count = {}
        with open('./jcdb/jcdb-movies.jsonlines', mode='r') as f_r:
            for line in f_r.readlines():
                obj = json.loads(line)
                if obj['カテゴリー'] == '成人映画' or obj['レーティング'] == 'R18+':
                    continue

                if len(obj['出演者']) != 0:
                    obj['出演者'] = list(
                        filter(lambda x: x['名前'] != None, obj['出演者']))
                    obj['出演者'].sort(key=lambda x: x['名前'])

                for c_f in obj['出演者']:
                    name_f = c_f['名前']
                    if name_f not in co_starring_count:
                        co_starring_count[name_f] = {}

                    for c_t in obj['出演者']:
                        name_t = c_t['名前']
                        if name_t not in co_starring_count[name_f]:
                            co_starring_count[name_f][name_t] = 1
                        else:
                            co_starring_count[name_f][name_t] += 1
        for name_f in co_starring_count.keys():
            c = 0
            for name_t in co_starring_count[name_f].keys():
                c += co_starring_count[name_f][name_t]
            write_data.append([[name_f, c]])

        for name_f in co_starring_count.keys():
            average_degree += len(co_starring_count[name_f].keys())
            if len(co_starring_count[name_f].keys()) in degree:
                degree[len(co_starring_count[name_f].keys())] += 1
            else:
                degree[len(co_starring_count[name_f].keys())] = 1

        average_degree /= len(co_starring_count.keys())
        # write_data.append([average_degree, edge_count])
        # write_data.append(['次数', '個数'])
        # for key in sorted(degree.keys()):
        #     write_data.append([key, degree[key]])

        writer.writerows(write_data)


if __name__ == '__main__':
    main()
