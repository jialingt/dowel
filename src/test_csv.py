import dowel
from dowel import logger, tabular

logger.add_output(dowel.StdOutput())
logger.add_output(dowel.CsvOutput('out.csv'))
logger.add_output(dowel.TensorBoardOutput('tensorboard_logdir'))

logger.log('Starting up...')
for i in range(4):
    logger.push_prefix('itr {} '.format(i))
    logger.log('Running training step')

    tabular.record('itr', i)
    tabular.record('loss', 100.0 / (2 + i))
    # Test 1
    # the addition of new data to tabular breaks logging to CSV
    if i == 2:
        tabular.record('new_data', i)

    # Test 2
    # Reduction of new data
    if i == 3:
        tabular.delete('loss')

    logger.log(tabular)

    logger.pop_prefix()
    logger.dump_all()

# Test 3
# Keep the number of header the same but different content
logger.push_prefix('itr {} '.format(4))
logger.log('Running training step')

tabular.record('itr', 4)
tabular.record('loss', 100.0 / (2 + i))
tabular.record('new_name', 0)
tabular.delete('new_data')
logger.log(tabular)

logger.pop_prefix()
logger.dump_all()

# Test 4
# Keep the number of header the same but different content
logger.push_prefix('itr {} '.format(5))
logger.log('Running training step')
tabular.delete('new_name')
tabular.delete('loss')
tabular.record('itr', 5)
tabular.record('reduce_num', 100.0 / (2 + 5))
tabular.record('new_data', 2)
logger.log(tabular)

logger.pop_prefix()
logger.dump_all()

logger.remove_all()