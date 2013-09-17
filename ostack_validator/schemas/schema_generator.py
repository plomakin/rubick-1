import argparse
import sys


class SchemaParser(object):

    def parse_args(self, argv):
        parser = argparse.ArgumentParser()
        parser.add_argument('--conf', dest='conf_file', default=None,
                            help='Path to configuration file sample')
        parser.add_argument('--project_name', dest='prj_name', default='nova',
                            help='Name of the configurations project')
        parser.add_argument('--config_version', dest='conf_ver',
                            default='2013.1', help='Version of the package')
        args = parser.parse_args(argv[1:])
        return args

    def variable_type_detection(self, variable):
        return basestring

    def generate_schema(self, file_to_open, file_to_generate='/tmp/sample.py'):
        with open(file_to_open, 'r') as f:
            content = f.readlines()
        with open(file_to_generate, 'w') as f:
            f.write("""from ostack_validator.schema import ConfigSchemaRegistry

nova = ConfigSchemaRegistry.register_schema(project='%s')

nova.version('%s')

""" % (self.prj_name, self.conf_ver)
            )
            for index, line in enumerate(content):
                print line
                if str(line).startswith('['):
                    f.write("nova.section('%s')\n\n" % str(line).strip('[]\n'))
                    continue
                if str(line).startswith('# ') or str(line).startswith(
                        '\n') or str(line).startswith('#\n'):
                    continue
                else:
                    revers_list = content[0:index]
                    revers_list.reverse()
                    comments = []
                    for comment in revers_list:
                        if str(comment).startswith('# '):
                            comments.append(comment)
                        else:
                            break
                    comments.reverse()
                    for comment in comments:
                        f.write(comment)
                    wrk_str = str(line).strip('#[]\n')
                    f.write(
                        "nova.param('%s', type='string', default='%s')\n\n" % (
                            wrk_str.split('=')[0], wrk_str.split('=')[1]))
                    continue

    def run(self, argv):
        args = self.parse_args(argv)
        params = vars(args)
        self.conf_file = params.pop('conf_file')
        self.prj_name = params.pop('prj_name')
        self.conf_ver = params.pop('conf_ver')
        self.generate_schema(self.conf_file)


if __name__ == '__main__':
    runner = SchemaParser()
    runner.run(sys.argv)